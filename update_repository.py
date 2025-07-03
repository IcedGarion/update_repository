'''
    Aggiorna tutti i repository facendo git pull del branch indicato e ricompilando il progetto con mvn install.
    I comandi eseguiti sono:
    - git fetch
    - git stash (in caso ci siano delle modifiche locali)
    - git checkout <branch>
    - git pull --rebase origin <branch>
    - mvn clean install -DskipTests
    
    Configurazione:
    repositories: elenco dei repository da aggiornare, con relativo branch di cui fare pull
    repo_main_dir: la directory contenente tutti i repository
    
    Esecuzione:
    python update_repository.py. 
    Il file deve essere allo stesso livello della cartella repo_main_dir, in cui sono contenuti tutti i repository
    python3, git e mvn installati
    per git, serve essere autenticati ai repository (tramite ssh) altrimenti per ogni repository viene richiesta l'autenticazione manuale
'''

import os, time, argparse, subprocess, json, config
from datetime import timedelta
from collections import OrderedDict

# Global var class
class Configuration:

    def __init__(self):
        self.log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")
        self.colors = {"red": '\033[91m', "yellow": '\033[93m', "green": '\033[92m', "end": '\033[0m'}

        # Vars for logging
        self.error_report = []
        self.times = dict()
        
        self.load_config_file(config)
        
    def load_config_file(self, new_config):
        # From config file
        self.config_repo_main_dir = new_config.repo_main_dir
        self.config_repositories = new_config.repositories
        self.config_mvn_exclusions = new_config.mvn_exclusions
        self.config_blacklist = new_config.blacklist

        # calc default repositories to scan, git / mvn and exclude blacklisted, based on config file
        self.git_repositories = OrderedDict({ repo: branch for repo, branch in new_config.repositories.items() if repo not in new_config.blacklist })
        self.mvn_repositories = [ repo for repo, branch in new_config.repositories.items() if repo not in new_config.mvn_exclusions ]
        
        # cmd output analysis
        self.git_output = { repo: "" for repo, branch in self.git_repositories.items() }
        self.mvn_output = { repo: "" for repo in self.mvn_repositories }

        # Vars for logging
        self.error_report = []
        self.times = dict()
        

configuration = Configuration()


# Functions
def check_dir():
    # main repo directory
    if(not os.path.isdir(configuration.config_repo_main_dir)):
        print("ERROR: missing main directory: {}".format(os.path.join(os.getcwd(), configuration.config_repo_main_dir)))
        exit(1)
        
    # log directory
    if(not os.path.isdir(configuration.log_dir)):
        os.makedirs(configuration.log_dir)


def analyze_git_output(repo: str, branch: str, output: str):
    if "No local changes to save" in output:
        configuration.git_output[repo] += "Nothing to stash, "
    else:
        configuration.git_output[repo] += configuration.colors["red"] + "Stashed changes" + configuration.colors["end"] + ", "
    
    if "Already on" in output:
        configuration.git_output[repo] += "Already on branch {}, ".format(branch)
    else:
        configuration.git_output[repo] +=  configuration.colors["yellow"] + "Checkout branch {}".format(branch) + configuration.colors["end"] + ", "
        
    if "Already up to date." in output:
        configuration.git_output[repo] += "Already up-to-date, "
    else:
        configuration.git_output[repo] += configuration.colors["green"] + "Pulled updates" + configuration.colors["end"] + ", "
        
    if "Your branch is up to date with" in output:
        configuration.git_output[repo] += "Nothing new to push on branch"


def git_command(abs_repo_path, branch, repo_dir):
    output = ""
    
    # Open log file
    with open(os.path.join(configuration.log_dir, "git-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        cmd = subprocess.Popen("cd " + abs_repo_path + " && git fetch && git stash && git checkout " + branch + " && git pull --rebase origin " + branch, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            
            # store output for analysis
            output += line.decode("utf-8")
            
            if not configuration.args.silent:
                print(line.decode("utf-8"), end='')
            output_file.write(line)
            
        cmd.wait()
    
    analyze_git_output(repo_dir, branch, output)
    
    return cmd.returncode    

  
def analyze_mvn_output(repo: str, output: str):
    if "BUILD SUCCESS" in output:
        configuration.mvn_output[repo] = configuration.colors["green"] + "Mvn build Success" + configuration.colors["end"]
    elif "BUILD FAILURE" in output:
        configuration.mvn_output[repo] = configuration.colors["red"] + "Mvn Build FAILURE" + configuration.colors["end"]
      

def mvn_command(abs_repo_path, repo_dir):
    output = ""    
    
    # Skip mvn step if git already up-to-date
    if "Already up-to-date" in configuration.git_output[repo_dir] and not configuration.args.force_maven:
        print("Skipped Mvn build (project already up-to-date)")
        configuration.mvn_output[repo_dir] = "Skipped Mvn build (project already up-to-date)"
        return 0    
    
    # Open log file
    with open(os.path.join(configuration.log_dir, "mvn-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        if configuration.args.test:
            cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install", \
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install -DskipTests", \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            # store output for analysis
            output += line.decode("utf-8")
            
            if not configuration.args.silent:
                print(line.decode("utf-8").replace("BUILD SUCCESS", configuration.colors["green"] + "BUILD SUCCESS" + configuration.colors["end"]).replace("BUILD FAILURE", configuration.colors["red"] + "BUILD FAILURE" + configuration.colors["end"]), end='')
            output_file.write(line)
            
        cmd.wait()
        
    analyze_mvn_output(repo_dir, output)

    return cmd.returncode    
    

def git_step():
    # Git pull
    git_count = 0
    git_total = len(configuration.git_repositories)
    width = os.get_terminal_size().columns
    
    print(configuration.colors["red"] + "="*int(width-15) + " GIT PULL STEP" + configuration.colors["end"])
    print("Git repo: {}".format([x for x,y in configuration.git_repositories.items()]))
    for repo_dir, branch in configuration.git_repositories.items():
        git_count += 1
        abs_repo_path = os.path.join(configuration.config_repo_main_dir, repo_dir)
        
        # execution time init
        configuration.times["git"].update({repo_dir: dict()})
        git_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            configuration.error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            git_end = time.time()
            configuration.times["git"][repo_dir].update({"start": git_start})
            configuration.times["git"][repo_dir].update({"end": git_end})
            continue
        
        # Git pull abs_repo_path
        print(configuration.colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(git_count))+len(str(git_total))+7)) + " " + repo_dir + " ({} / {})".format(git_count, git_total) + configuration.colors["end"])
        print("> cd {}, git stash && git checkout {} && git pull --rebase origin {}".format(abs_repo_path, branch, branch))
        print()
        
        # EXEC COMMAND
        exit_code = git_command(abs_repo_path, branch, repo_dir)
        
        # error git pull
        if(exit_code != 0):
            configuration.error_report.append("{}: git step error ({})".format(repo_dir, "cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch))
        
        # execution time calc
        git_end = time.time()
        configuration.times["git"][repo_dir].update({"start": git_start})
        configuration.times["git"][repo_dir].update({"end": git_end})
        
    configuration.times.update({ "git_end": time.time() })


def mvn_step():
    # Mvn install
    mvn_count = 0
    mvn_total = len(configuration.mvn_repositories)
    width = os.get_terminal_size().columns
    configuration.times.update({ "mvn_start": time.time() })
    
    print(configuration.colors["red"] + "="*int(width-18) + " MVN INSTALL STEP"+ configuration.colors["end"])
    print("Mvn repo: {}".format([x for x in configuration.mvn_repositories]))
    for repo_dir in configuration.mvn_repositories:
        mvn_count += 1
        width = os.get_terminal_size().columns
        abs_repo_path = os.path.join(configuration.config_repo_main_dir, repo_dir)
        
        # execution time init
        configuration.times["mvn"].update({repo_dir: dict()})
        mvn_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            configuration.error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            mvn_end = time.time()
            configuration.times["mvn"][repo_dir].update({"start": mvn_start})
            configuration.times["mvn"][repo_dir].update({"end": mvn_end})
            continue
        
        print(configuration.colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(mvn_count))+len(str(mvn_total))+7)) + " " + repo_dir + " ({} / {})".format(mvn_count, mvn_total) + configuration.colors["end"])
        
        if configuration.args.test:
            print("> cd {}, mvn clean install".format(abs_repo_path))
            print()
        else:
            print("> cd {}, mvn clean install -DskipTests".format(abs_repo_path))
            print()
        
        # EXEC COMMAND
        exit_code = mvn_command(abs_repo_path, repo_dir)
        
        # error mvn install
        if(exit_code != 0):
            configuration.error_report.append("{}: mvn install step error".format(repo_dir))
            
        # execution time calc
        mvn_end = time.time()
        configuration.times["mvn"][repo_dir].update({"start": mvn_start})
        configuration.times["mvn"][repo_dir].update({"end": mvn_end})
        
    configuration.times.update({ "mvn_end": time.time() })


def error_report():
    width = os.get_terminal_size().columns
    print(configuration.colors["red"] + "="*int(width-4) + " END" + configuration.colors["end"])
    if(len(configuration.error_report) == 0):
        print("ERROR REPORT: " + configuration.colors["green"] + "OK!!" + configuration.colors["end"])
    else:
        print("ERROR REPORT: " + configuration.colors["red"] + "ERRORS..." + configuration.colors["end"])
        print('\n'.join([x for x in configuration.error_report]))
        
    # Execution time report
    print()
    print("Execution time:")
    print("Total: {}. git: {}, mvn: {}".format(str(timedelta(seconds=configuration.times["end"] - configuration.times["start"])).split('.')[0], str(timedelta(seconds=configuration.times["git_end"] - configuration.times["start"])).split('.')[0], str(timedelta(seconds=configuration.times["mvn_end"] - configuration.times["git_end"])).split('.')[0]))
    print()
    for repo_dir, branch in configuration.git_repositories.items():
        padding = max([len(repo) for repo, branch in configuration.git_repositories.items()])
        print(repo_dir.ljust(padding) + ": git step: {} - {}".format(str(timedelta(seconds=configuration.times["git"][repo_dir]["end"] - configuration.times["git"][repo_dir]["start"])).split('.')[0],  configuration.git_output[repo_dir]))
        
        if(repo_dir in configuration.mvn_repositories):
            print(" "*padding + "  mvn step: {} - {}".format(str(timedelta(seconds=configuration.times["mvn"][repo_dir]["end"] - configuration.times["mvn"][repo_dir]["start"])).split('.')[0],  configuration.mvn_output[repo_dir]))
    

def parse_args():
    parser = argparse.ArgumentParser(prog='Repository update', description='Update all your local repositories by git pulling the specified branch and recompiling the project with maven install')
    parser.add_argument('-t', '--test', action="store_true", help="Run maven tests during mvn install (default false)")
    parser.add_argument('-g', '--git-step-only', action="store_true", help="Only execute git pull step (on repositories in config or in --git arg)")
    parser.add_argument('-m', '--mvn-step-only', action="store_true", help="Only execute mvn install step (on repositories in config or in --mvn arg)")
    parser.add_argument('-s', '--silent', action="store_true", help="Suppress output print (default false)")
    parser.add_argument('--git-only', type=str, metavar="<repository:branch ordered dict> (ex: \"{'resevo-parent':'develop','resevo-apigw-service':'develop'}\")", help="List repositories to git pull only (overrides configuration file)")
    parser.add_argument('--mvn-only', type=str, metavar="<repository list> (ex: \"resevo-parent,resevo-apigw-service\")", help="List repositories to mvn install only (overrides configuration file)")
    parser.add_argument('--only', type=str, metavar="<repository:branch ordered dict> (ex: \"{'resevo-parent':'develop','resevo-apigw-service':'develop'}\")", help="List repositories to git pull + mvn install (overrides configuration file)")
    parser.add_argument('--git-except', type=str, metavar="<repository list> (ex: \"resevo-parent,resevo-apigw-service\")", help="List repositories to exclude from git pull step (overrides configuration file)")
    parser.add_argument('--mvn-except', type=str, metavar="<repository list> (ex: \"resevo-parent,resevo-apigw-service\")", help="List repositories to exclude from mvn install step (overrides configuration file)")
    parser.add_argument('--all-except', type=str, metavar="<repository list> (ex: \"resevo-parent,resevo-apigw-service\")", help="List repositories to exclude from git pull + mvn install (overrides configuration file)")    
    parser.add_argument('--force-maven', action="store_true", help="Run maven install step even if git project is already up-to-date (default false)")
    parser.add_argument('--config-file', type=str, help="Specify a custom config file")
    
    configuration.args = parser.parse_args()
    

# Compute git and maven repositories lists, based on program parameters
def calc_repos():
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
        
    # Override config file if specified
    if configuration.args.config_file:
        configuration.config_file = configuration.args.config_file
        
        try:
            import importlib
            new_config = importlib.import_module(configuration.config_file.split('.')[0])        
            configuration.load_config_file(new_config)
        except Exception as e:
            print("Error loading custom configuration file: " + configuration.config_file)
            print(e)
            exit(1)


    # --git-step-only
    if configuration.args.git_step_only:
        configuration.mvn_repositories = []
    
    # --mvn-step-only
    if configuration.args.mvn_step_only:
        configuration.git_repositories = dict()
        
    # --git-only
    if configuration.args.git_only:
        try:
            configuration.git_repositories = decoder.decode(configuration.args.git_only.replace(" ", "").replace("'", '"'))
        except json.decoder.JSONDecodeError as e:
            print("Error decoding --git-only parameter (double check quotes!)")
            print(e)
            exit(1)
        
    # --mvn-only
    if configuration.args.mvn_only:
        configuration.mvn_repositories = configuration.args.mvn_only.replace(" ", "").split(',')
    
    # --only
    if configuration.args.only:
        try:
            configuration.git_repositories = decoder.decode(configuration.args.only.replace(" ", "").replace("'", '"'))
            configuration.mvn_repositories = [ repo for repo, branch in decoder.decode(configuration.args.only.replace(" ", "").replace("'", '"')).items() ]
        except json.decoder.JSONDecodeError as e:
            print("Error decoding --only parameter (double check quotes!)")
            print(e)
            exit(1)
    
    # --git-except
    if configuration.args.git_except:
        configuration.git_repositories = OrderedDict( (repo, branch) for repo, branch in configuration.git_repositories.items() if repo not in configuration.args.git_except.replace(" ", "").split(','))
    
    # --mvn-except
    if configuration.args.mvn_except:
        configuration.mvn_repositories = [ repo for repo in configuration.mvn_repositories if repo not in configuration.args.mvn_except.replace(" ", "").split(',') ]
        
    # --all-except = git-except + mvn-except
    if configuration.args.all_except:
        configuration.git_repositories = OrderedDict( (repo, branch) for repo, branch in configuration.git_repositories.items() if repo not in configuration.args.all_except.replace(" ", "").split(','))
        configuration.mvn_repositories = [ repo for repo in configuration.mvn_repositories if repo not in configuration.args.all_except.replace(" ", "").split(',') ]

# MAIN
if __name__ == "__main__":

    # parse program parameters
    parse_args()
    
    # check directories (log, main repository)
    check_dir()
    
    # parse parameters to determine repository lists to work on (git / mvn)
    calc_repos()
    
    # START
    print("START")
    configuration.times.update({ "start": time.time() })
    configuration.times.update({ "git": dict(), "mvn": dict() })
    
    # git pull
    git_step()
    
    # mvn install
    mvn_step()

    # END
    configuration.times.update({ "end": time.time() })
    
    # print errors and execution time
    error_report()
    
# TODO: un readme
# quando fai KILL con ctrl+c, intercettare, e stoppare TUTTI i procesi figli lanciati, altrimenti loro vanno avanti di sotto 
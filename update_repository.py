'''
    Aggiorna tutti i repository facendo git pull del branch indicato e ricompilando il progetto con mvn install.
    I comandi eseguiti sono:
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

import os, time, argparse, subprocess, json
from datetime import timedelta
from config import *


# Global var class
class Configuration:
    log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")
    colors = {"red": '\033[91m', "yellow": '\033[93m', "green": '\033[92m', "end": '\033[0m'}

    # From config file
    config_repo_main_dir = repo_main_dir
    config_repositories = repositories
    config_mvn_exclusions = mvn_exclusions
    config_blacklist = blacklist

    # calc repositories to scan, git / mvn and exclude blacklisted
    git_repositories = OrderedDict({ repo: branch for repo, branch in repositories.items() if repo not in blacklist })
    mvn_repositories = [ repo for repo, branch in repositories.items() if repo not in mvn_exclusions ]

    # Vars for logging
    error_report = []
    times = dict()



# Functions
def check_dir():
    # main repo directory
    if(not os.path.isdir(Configuration.config_repo_main_dir)):
        print("ERROR: missing main directory: {}".format(os.path.join(os.getcwd(), Configuration.config_repo_main_dir)))
        exit(1)
        
    # log directory
    if(not os.path.isdir(Configuration.log_dir)):
        os.makedirs(Configuration.log_dir)


def git_command(abs_repo_path, branch, repo_dir):
    # Open log file
    with open(os.path.join(Configuration.log_dir, "git-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        cmd = subprocess.Popen("cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            
            if not Configuration.args.silent:
                print(line.decode("utf-8"), end='')
            output_file.write(line)
            
        cmd.wait()
    
    return cmd.returncode    
    

def mvn_command(abs_repo_path, repo_dir):
    # Open log file
    with open(os.path.join(Configuration.log_dir, "mvn-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        if Configuration.args.test:
            cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install", \
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install -DskipTests", \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            if not Configuration.args.silent:
                print(line.decode("utf-8").replace("BUILD SUCCESS", Configuration.colors["green"] + "BUILD SUCCESS" + Configuration.colors["end"]).replace("BUILD FAILURE", Configuration.colors["red"] + "BUILD FAILURE" + Configuration.colors["end"]), end='')
            output_file.write(line)
            
        cmd.wait()

    return cmd.returncode    
    

def git_step():
    # Git pull
    git_count = 0
    git_total = len(Configuration.git_repositories)
    width = os.get_terminal_size().columns
    
    print(Configuration.colors["red"] + "="*int(width-15) + " GIT PULL STEP" + Configuration.colors["end"])
    for repo_dir, branch in Configuration.git_repositories.items():
        git_count += 1
        abs_repo_path = os.path.join(Configuration.config_repo_main_dir, repo_dir)
        
        # execution time init
        Configuration.times["git"].update({repo_dir: dict()})
        git_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            Configuration.error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            git_end = time.time()
            Configuration.times["git"][repo_dir].update({"start": git_start})
            Configuration.times["git"][repo_dir].update({"end": git_end})
            continue
        
        # Git pull abs_repo_path
        print(Configuration.colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(git_count))+len(str(git_total))+7)) + " " + repo_dir + " ({} / {})".format(git_count, git_total) + Configuration.colors["end"])
        print("> cd {}, git stash && git checkout {} && git pull --rebase origin {}".format(abs_repo_path, branch, branch))
        
        # EXEC COMMAND
        exit_code = git_command(abs_repo_path, branch, repo_dir)
        
        # error git pull
        if(exit_code != 0):
            Configuration.error_report.append("{}: git step error ({})".format(repo_dir, "cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch))
        
        # execution time calc
        git_end = time.time()
        Configuration.times["git"][repo_dir].update({"start": git_start})
        Configuration.times["git"][repo_dir].update({"end": git_end})
        
    Configuration.times.update({ "git_end": time.time() })


def mvn_step():
    # Mvn install
    mvn_count = 0
    mvn_total = len(Configuration.mvn_repositories)
    width = os.get_terminal_size().columns
    Configuration.times.update({ "mvn_start": time.time() })
    
    print(Configuration.colors["red"] + "="*int(width-18) + " MVN INSTALL STEP"+ Configuration.colors["end"])
    for repo_dir in Configuration.mvn_repositories:
        mvn_count += 1
        width = os.get_terminal_size().columns
        abs_repo_path = os.path.join(Configuration.config_repo_main_dir, repo_dir)
        
        # execution time init
        Configuration.times["mvn"].update({repo_dir: dict()})
        mvn_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            Configuration.error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            mvn_end = time.time()
            Configuration.times["mvn"][repo_dir].update({"start": mvn_start})
            Configuration.times["mvn"][repo_dir].update({"end": mvn_end})
            continue
        
        print(Configuration.colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(mvn_count))+len(str(mvn_total))+7)) + " " + repo_dir + " ({} / {})".format(mvn_count, mvn_total) + Configuration.colors["end"])
        
        if Configuration.args.test:
            print("> cd {}, mvn clean install".format(abs_repo_path))
        else:
            print("> cd {}, mvn clean install -DskipTests".format(abs_repo_path))
        
        # EXEC COMMAND
        exit_code = mvn_command(abs_repo_path, repo_dir)
        
        # error mvn install
        if(exit_code != 0):
            Configuration.error_report.append("{}: mvn install step error".format(repo_dir))
            
        # execution time calc
        mvn_end = time.time()
        Configuration.times["mvn"][repo_dir].update({"start": mvn_start})
        Configuration.times["mvn"][repo_dir].update({"end": mvn_end})
        
    Configuration.times.update({ "mvn_end": time.time() })


def error_report():
    width = os.get_terminal_size().columns
    print(Configuration.colors["red"] + "="*int(width-4) + " END" + Configuration.colors["end"])
    if(len(Configuration.error_report) == 0):
        print("ERROR REPORT: " + Configuration.colors["green"] + "OK!!" + Configuration.colors["end"])
    else:
        print("ERROR REPORT: " + Configuration.colors["red"] + "ERRORS..." + Configuration.colors["end"])
        print('\n'.join([x for x in Configuration.error_report]))
        
    # Execution time report
    print()
    print("Execution time:")
    print("Total: {}. git: {}, mvn: {}".format(str(timedelta(seconds=Configuration.times["end"] - Configuration.times["start"])).split('.')[0], str(timedelta(seconds=Configuration.times["git_end"] - Configuration.times["start"])).split('.')[0], str(timedelta(seconds=Configuration.times["mvn_end"] - Configuration.times["git_end"])).split('.')[0]))
    print()
    for repo_dir, branch in Configuration.git_repositories.items():
        padding = max([len(repo) for repo, branch in Configuration.git_repositories.items()])
        print(repo_dir.ljust(padding) + ": git step: {}".format(str(timedelta(seconds=Configuration.times["git"][repo_dir]["end"] - Configuration.times["git"][repo_dir]["start"])).split('.')[0]))
        
        if(repo_dir in Configuration.mvn_repositories):
            print(" "*padding + "  mvn step: {}".format(str(timedelta(seconds=Configuration.times["mvn"][repo_dir]["end"] - Configuration.times["mvn"][repo_dir]["start"])).split('.')[0]))
    

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
    
    Configuration.args = parser.parse_args()
    

# Compute git and maven repositories lists, based on program parameters
def calc_repos():
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    # --git-step-only
    if Configuration.args.git_step_only:
        Configuration.mvn_repositories = []
    
    # --mvn-step-only
    if Configuration.args.mvn_step_only:
        Configuration.git_repositories = dict()
        
    # --git-only
    if Configuration.args.git_only:
        try:
            Configuration.git_repositories = decoder.decode(Configuration.args.git_only.replace(" ", "").replace("'", '"'))
        except json.decoder.JSONDecodeError as e:
            print("Error decoding --git-only parameter (double check quotes!)")
            print(e)
            exit(1)
        
    # --mvn-only
    if Configuration.args.mvn_only:
        Configuration.mvn_repositories = Configuration.args.mvn_only.replace(" ", "").split(',')
    
    # --only
    if Configuration.args.only:
        try:
            Configuration.git_repositories = decoder.decode(Configuration.args.only.replace(" ", "").replace("'", '"'))
            Configuration.mvn_repositories = [ repo for repo, branch in decoder.decode(Configuration.args.only.replace(" ", "").replace("'", '"')).items() ]
        except json.decoder.JSONDecodeError as e:
            print("Error decoding --only parameter (double check quotes!)")
            print(e)
            exit(1)
    
    # --git-except
    if Configuration.args.git_except:
        Configuration.git_repositories = OrderedDict( (repo, branch) for repo, branch in Configuration.git_repositories.items() if repo not in Configuration.args.git_except.replace(" ", "").split(','))
    
    # --mvn-except
    if Configuration.args.mvn_except:
        Configuration.mvn_repositories = [ repo for repo in Configuration.mvn_repositories if repo not in Configuration.args.mvn_except.replace(" ", "").split(',') ]
        
    # --all-except = git-except + mvn-except
    if Configuration.args.all_except:
        Configuration.git_repositories = OrderedDict( (repo, branch) for repo, branch in Configuration.git_repositories.items() if repo not in Configuration.args.all_except.replace(" ", "").split(','))
        Configuration.mvn_repositories = [ repo for repo in Configuration.mvn_repositories if repo not in Configuration.args.all_except.replace(" ", "").split(',') ]

# MAIN
if __name__ == "__main__":

    # parse program parameters
    parse_args()
    
    # check directories (log, main repository)
    check_dir()
    
    # parse parameters to determine repository lists to work on (git / mvn)
    calc_repos()
    
    # START
    Configuration.times.update({ "start": time.time() })
    Configuration.times.update({ "git": dict(), "mvn": dict() })
    
    # git pull
    git_step()
    
    # mvn install
    mvn_step()

    # END
    Configuration.times.update({ "end": time.time() })
    
    # print errors and execution time
    error_report()
    

# TODO: 

# 1. report finale deve dire (per ciascun projetto): se ha stashato, se hai pullato roba nuova oppure no, se la mvn install è andata o no

# MANCA --force-maven

# A INIZIO MVN STEP E GIT STEP, ELENCARE NOME DEI REPO SU CUI SI STA PER OPERARE
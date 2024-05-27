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

import os, time, argparse, subprocess
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
            print(line.decode("utf-8"), end='')
            output_file.write(line)
            
        cmd.wait()
    
    return cmd.returncode    
    

def mvn_command(abs_repo_path, repo_dir):
    # Open log file
    with open(os.path.join(Configuration.log_dir, "mvn-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install -DskipTests", \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            print(line.decode("utf-8").replace("BUILD SUCCESS", Configuration.colors["green"] + "BUILD SUCCESS" + Configuration.colors["end"]).replace("BUILD FAILURE", Configuration.colors["red"] + "BUILD FAILURE" + Configuration.colors["end"]), end='')
            output_file.write(line)
            
        cmd.wait()

    return cmd.returncode    
    


def main():
    
    
    
    # Start
    Configuration.times.update({ "start": time.time() })
    Configuration.times.update({ "git": dict(), "mvn": dict() })
     
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
        
        # error git pull
        if(exit_code != 0):
            Configuration.error_report.append("{}: git step error ({})".format(repo_dir, "cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch))
        
        # execution time calc
        git_end = time.time()
        Configuration.times["git"][repo_dir].update({"start": git_start})
        Configuration.times["git"][repo_dir].update({"end": git_end})
        
    git_end = time.time()
    
    # Mvn install
    mvn_count = 0
    mvn_total = len(Configuration.mvn_repositories)
    width = os.get_terminal_size().columns
    
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


    # END
    mvn_end = time.time()
    Configuration.times.update({ "end": time.time() })
    
    # Error report
    padding = max([len(repo) for repo, branch in Configuration.git_repositories.items()])
    width = os.get_terminal_size().columns
    print(Configuration.colors["red"] + "="*int(width-4) + " END" + Configuration.colors["end"])
    if(len(Configuration.error_report) == 0):
        print("ERROR REPORT: " + Configuration.colors["green"] + "OK!!" + Configuration.colors["end"])
    else:
        print("ERROR REPORT: " + Configuration.colors["red"] + "ERRORS..." + Configuration.colors["end"])
        print('\n'.join([x for x in Configuration.error_report]))
        
    # Execution time report
    print("Execution time:")
    print("Total: {}. git: {}, mvn: {}".format(str(timedelta(seconds=Configuration.times["end"] - Configuration.times["start"])).split('.')[0], str(timedelta(seconds=git_end - Configuration.times["start"])).split('.')[0], str(timedelta(seconds=mvn_end - git_end)).split('.')[0]))
    print()
    for repo_dir, branch in Configuration.git_repositories.items():
        print(repo_dir.ljust(padding) + ": git step: {}".format(str(timedelta(seconds=Configuration.times["git"][repo_dir]["end"] - Configuration.times["git"][repo_dir]["start"])).split('.')[0]))
        
        if(repo_dir in Configuration.mvn_repositories):
            print(" "*padding + "  mvn step: {}".format(str(timedelta(seconds=Configuration.times["mvn"][repo_dir]["end"] - Configuration.times["mvn"][repo_dir]["start"])).split('.')[0]))
    

def parse_args():
    parser = argparse.ArgumentParser(prog='Repository update', description='Aggiorna tutti i repository facendo git pull del branch indicato e ricompilando il progetto con mvn install')
    parser.add_argument('-t', '--test', action="store_true", help="Run maven tests during mvn install (default false)")
    parser.add_argument('-g', '--git-step-only', action="store_true", help="Only execute git pull step (on repositories in config or in --git arg)")
    parser.add_argument('-m', '--mvn-step-only', action="store_true", help="Only execute mvn install step (on repositories in config or in --mvn arg)")
    parser.add_argument('-s', '--silent', action="store_true", help="Suppress output print (default false)")
    parser.add_argument('--git-only', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to git pull only (overrides configuration file)")
    parser.add_argument('--mvn-only', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to mvn install only (overrides configuration file)")
    parser.add_argument('--only', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to git pull + mvn install (overrides configuration file)")
    parser.add_argument('--git-except', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to exclude from git pull step (overrides configuration file)")
    parser.add_argument('--mvn-except', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to exclude from mvn install step (overrides configuration file)")
    parser.add_argument('--except', type=str, metavar="<repository list> (ex: resevo-parent-lib,resevo-apigw-service)", help="List repositories to exclude from git pull + mvn install (overrides configuration file)")    
    parser.add_argument('--force-maven', action="store_true", help="Run maven install step even if git project is already up-to-date (default false)")
    
    Configuration.args = parser.parse_args()
    


# MAIN
if __name__ == "__main__":
    

    
    # parse args
    parse_args()
    
    # check dirs (log, main repository)
    check_dir()
    
    main()
    

# TODO: 

# report finale deve dire (per ciascun projetto): se ha stashato, se hai pullato roba nuova oppure no, se la mvn install è andata o no

# implementare gli args: calcola innanzitutto la lista di repo (git e mvn) su cui devi eseguire, in base ai vari args

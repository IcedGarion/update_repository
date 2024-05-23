'''
    Aggiorna tutti i repository facendo git pull del branch indicato e ricompilando il progetto.
    I comandi eseguiti sono:
    - git stash (in caso ci siano delle modifiche locali)
    - git checkout <branch>
    - git pull --rebase origin <branch>
    - mvn clean install -DskipTests
    
    Configurazione:
    repos_branch: elenco dei repository da aggiornare, con relativo branch di cui fare pull
    repos_order: indica l'ordine con cui fare la build (prima le librerie, prima le dipendenze)
    repo_main_dir: la directory contenente tutti i repository
    (resevo-project viene ignorato perche' non compare nella lista)
    
    Esecuzione:
    python update_repository.py. 
    Il file deve essere allo stesso livello della cartella repo_main_dir, in cui sono contenuti tutti i repository
    python3, git e mvn installati
    per git, serve essere autenticati ai repository (tramite ssh) altrimenti per ogni repository viene richiesta l'autenticazione manuale
'''

import os, time, argparse, subprocess
from config import *

# Globals
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")

# Functions
def git_command(abs_repo_path, branch, repo_dir):
    # Open log file
    with open(os.path.join(log_dir, "git-{}.log".format(repo_dir)), 'wb') as output_file:
        
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
    with open(os.path.join(log_dir, "mvn-{}.log".format(repo_dir)), 'wb') as output_file:
        
        # Exec command
        cmd = subprocess.Popen("cd " + abs_repo_path + " && mvn clean install -DskipTests", \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
        # print on console and file
        for line in cmd.stdout:
            print(line.decode("utf-8"), end='')
            output_file.write(line)
            
        cmd.wait()

    return cmd.returncode    
    

def main():
    
    # For logging
    width = width = os.get_terminal_size().columns
    colors = {"red": '\033[91m', "yellow": '\033[93m', "green": '\033[92m', "end": '\033[0m'}
    error_report = []
    times = dict()
    git_count = 0
    git_total = len(repos_branch)
    mvn_count = 0
    mvn_total = len(repos_order)
    cmd_output = "/tmp/cmd_output.txt"
    
    
    # Init
    times.update({ "start": time.time() })
    times.update({"git": dict(), "mvn": dict()})
    
    
    # Check main directory
    if(not os.path.isdir(os.path.join(os.getcwd(), repo_main_dir))):
        print("ERROR: missing main directory: {}".format(os.path.join(os.getcwd(), repo_main_dir)))
        exit(1)
    
    # Git pull
    print(colors["red"] + "="*int(width-15) + " GIT PULL STEP" + colors["end"])
    for repo_dir, branch in repos_branch.items():
        git_count += 1
        width = width = os.get_terminal_size().columns
        abs_repo_path = os.path.join(repo_main_dir, repo_dir)
        
        # execution time init
        times["git"].update({repo_dir: dict()})
        git_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            git_end = time.time()
            times["git"][repo_dir].update({"start": git_start})
            times["git"][repo_dir].update({"end": git_end})
            continue
        
        # Git pull abs_repo_path
        print(colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(git_count))+len(str(git_total))+7)) + " " + repo_dir + " ({} / {})".format(git_count, git_total) + colors["end"])
        print("> cd {}, git stash && git checkout {} && git pull --rebase origin {}".format(abs_repo_path, branch, branch))
        
        # EXEC COMMAND
        exit_code = git_command(abs_repo_path, branch, repo_dir)
        
        # error git pull
        if(exit_code != 0):
            error_report.append("{}: git step error ({})".format(repo_dir, "cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch))
        
        # error git pull
        if(exit_code != 0):
            error_report.append("{}: git step error ({})".format(repo_dir, "cd " + abs_repo_path + " && git stash && git checkout " + branch + " && git pull --rebase origin " + branch))
        
        # execution time calc
        git_end = time.time()
        times["git"][repo_dir].update({"start": git_start})
        times["git"][repo_dir].update({"end": git_end})
        
    
    # Mvn install
    print(colors["red"] + "="*int(width-18) + " MVN INSTALL STEP"+ colors["end"])
    for repo_dir in repos_order:
        mvn_count += 1
        width = width = os.get_terminal_size().columns
        abs_repo_path = os.path.join(repo_main_dir, repo_dir)
        
        # execution time init
        times["mvn"].update({repo_dir: dict()})
        mvn_start = time.time()
        
        # error missing directory
        if(not os.path.isdir(abs_repo_path)):
            print("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            error_report.append("{}: missing directory: {}".format(repo_dir, abs_repo_path))
            
            # execution time calc
            mvn_end = time.time()
            times["mvn"][repo_dir].update({"start": mvn_start})
            times["mvn"][repo_dir].update({"end": mvn_end})
            continue
        
        print(colors["yellow"] + "-"*int(width-(len(repo_dir)+len(str(mvn_count))+len(str(mvn_total))+7)) + " " + repo_dir + " ({} / {})".format(mvn_count, mvn_total) + colors["end"])
        print("> cd {}, mvn clean install -DskipTests".format(abs_repo_path))
        
        # EXEC COMMAND
        exit_code = mvn_command(abs_repo_path, repo_dir)
        
        # error mvn install
        if(exit_code != 0):
            error_report.append("{}: mvn install step error".format(repo_dir))
       
            
        # execution time calc
        mvn_end = time.time()
        times["mvn"][repo_dir].update({"start": mvn_start})
        times["mvn"][repo_dir].update({"end": mvn_end})


    # END
    times.update({ "end": time.time() })
    
    # Error report
    print(colors["red"] + "="*int(width-4) + " END" + colors["end"])
    if(len(error_report) == 0):
        print("ERROR REPORT: " + colors["green"] + "OK!!" + colors["end"])
    else:
        print("ERROR REPORT: " + colors["red"] + "ERRORS..." + colors["end"])
        print('\n'.join([x for x in error_report]))
        
    # Execution time report
    print("Execution time:")
    print("Total: {:.3} seconds. git: {:.3}, mvn: {:.3}".format(times["end"] - times["start"], git_end - times["start"], mvn_end - git_end))
    for repo_dir, branch in repos_branch.items():
        print("{}: git step: {:.3} seconds".format(repo_dir, times["git"][repo_dir]["end"] - times["git"][repo_dir]["start"]))
        
        if(repo_dir in repos_order):
            print(" "*len(repo_dir) + ": mvn step: {:.3} seconds".format(repo_dir, times["mvn"][repo_dir]["end"] - times["mvn"][repo_dir]["start"]))
    

def parse_args():
    parser = argparse.ArgumentParser(prog='Repository update', description='Repository update')
    parser.add_argument('-t', '--test')
    # args = 
    

# MAIN
if __name__ == "__main__":
    
    
    # parse args
    
    # check dirs (log, repository, ...)
    
    main()
    

# TODO: 
# quanto ci mettono le singole fasi (da mostrare alla fine) + il totale
# per ciascun elemento della fase, sul suo nome '------' dire anche quanti ne mancano (1 / 10, 2 / 10, ...)
# -> da testare sti 2

# report finale deve dire (per ciascun projetto): se ha stashato, se hai pullato roba nuova oppure no, se la mvn install è andata o no
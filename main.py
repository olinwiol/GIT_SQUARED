import os
import subprocess
import argparse
import time


def folder_exists(language):
    return os.path.isdir(language)


def file_exists(language):
    return os.path.isfile(os.path.join(language, "main." + language))


def generate_folder(language):
    os.mkdir(language)


def generate_file(language):
    filename = os.path.join(language, "main." + language)
    with open(filename, "w") as f:
        f.write(f"// This is a {language} file.\n")


def remove_file(language):
    filename = os.path.join(language, "main." + language)
    os.remove(filename)


def remove_folder(language):
    if folder_exists(language):
        os.rmdir(language)


def generate_language_files(languages):
    for language in languages:
        if not folder_exists(language):
            generate_folder(language)
        if not file_exists(language):
            generate_file(language)


def remove_language_files(languages):
    for language in languages:
        if file_exists(language):
            remove_file(language)
        if folder_exists(language):
            remove_folder(language)


def get_languages():
    with open("languages.txt", "r") as f:
        lines = f.readlines()
    languages = [line.strip() for line in lines if not line.startswith("#")]
    return languages


def initialize_subprocess(git_token, username, commit_message, repository, first_run):
    languages = get_languages()
    os.chdir(os.path.dirname(__file__) + "/" + repository)

    if first_run:
        # Set up Git for the first run
        repo_url = f"https://{username}:{git_token}@github.com/{username}/{repository}.git"
        subprocess.run(["git", "init"])
        subprocess.run(["git", "config", "user.name", username])
        subprocess.run(["git", "config", "user.email", f"{username}@gmail.com"])
        subprocess.run(["git", "remote", "add", "origin", repo_url])

    while True:
        # Step 1: Generate files
        print("Generating files...")
        generate_language_files(languages)
        print("Files generated.")

        # Step 2: Add, commit, and push generated files
        print("Adding and committing files...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push", "-u", "origin", "master"])
        print("Files pushed.")

        # Step 3: Remove files
        print("Removing files...")
        remove_language_files(languages)
        print("Files removed.")

        # Step 4: Commit and push file removal
        print("Committing file removal...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Removed files: {commit_message}"])
        subprocess.run(["git", "push", "origin", "master"])
        print("File removal pushed.")

        # Wait 5 minutes before repeating
        print("Waiting for 5 minutes before repeating...")
        time.sleep(30)  # 300 seconds = 5 minutes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate file creation, commit, push, and removal.")
    parser.add_argument('--git_token', required=False, help="Your GIT token for authentication.")
    parser.add_argument('--username', required=False, help="Your GIT username.")
    parser.add_argument('--commit_message', required=False, help="Custom commit message.")
    parser.add_argument('--repository', required=False, help="The repository folder name.")
    parser.add_argument('--first_run', type=bool, required=False, help="Set to True if running for the first time.")
    parser.add_help = True
    args = parser.parse_args()

    git_token = args.git_token if args.git_token else "YOURGITTOKEN"
    username = args.username if args.username else "YOURUSERNAME"
    commit_message = args.commit_message if args.commit_message else "Automated commit message"
    repository = args.repository if args.repository else "REPOSITORYNAME"
    first_run = args.first_run if args.first_run else False

    initialize_subprocess(git_token, username, commit_message, repository, first_run)
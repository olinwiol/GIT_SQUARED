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


# Function to generate files with appropriate code for each language
def generate_file(language):
    filename = os.path.join(language, "main." + language)
    code_snippets = {
        "c": "#include <stdio.h>\nint main() { printf(\"Hello, C!\\n\"); return 0; }",
        "cs": "using System;\nclass Program { static void Main() { Console.WriteLine(\"Hello, C#!\"); } }",
        "py": "print(\"Hello, Python!\")",
        "java": "public class Main { public static void main(String[] args) { System.out.println(\"Hello, Java!\"); } }",
        "cpp": "#include <iostream>\nint main() { std::cout << \"Hello, C++!\" << std::endl; return 0; }",
        "js": "console.log(\"Hello, JavaScript!\");",
        "php": "<?php\necho \"Hello, PHP!\";\n?>",
        "go": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello, Go!\") }",
        "rb": "puts \"Hello, Ruby!\"",
        "swift": "print(\"Hello, Swift!\")",
        "kt": "fun main() { println(\"Hello, Kotlin!\") }",
        "r": "print(\"Hello, R!\")",
        "sql": "-- SQL Example\nSELECT 'Hello, SQL';",
        "pl": "print \"Hello, Perl!\\n\";",
        "m": "disp('Hello, MATLAB!');",
        "lua": "print(\"Hello, Lua!\")",
        "hs": "main = putStrLn \"Hello, Haskell!\""
    }
    # Write appropriate code to the file
    with open(filename, "w") as f:
        f.write(code_snippets.get(language, f"// No code snippet available for {language}"))
    print(f"Generated file: {filename}")


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

        # Step 3: Wait for 5 minutes before removing files
        print("Files will remain for 5 minutes...")
        time.sleep(300)  # 300 seconds = 5 minutes

        # Step 4: Remove files
        print("Removing files...")
        remove_language_files(languages)
        print("Files removed.")

        # Step 5: Commit and push file removal
        print("Committing file removal...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Removed files: {commit_message}"])
        subprocess.run(["git", "push", "origin", "master"])
        print("File removal pushed.")

        # Step 6: Wait for another 5 minutes before restarting the loop
        print("Waiting for 5 minutes before regenerating files...")
        time.sleep(300)  # 300 seconds = 5 minutes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate file creation, commit, push, and removal.")
    parser.add_argument('--repo_url', required=False, help="The URL of the repository.")
    parser.add_argument('--git_token', required=False, help="Your GIT token for authentication.")
    parser.add_argument('--username', required=False, help="Your GIT username.")
    parser.add_argument('--commit_message', required=False, help="Custom commit message.")
    parser.add_argument('--repository', required=False, help="The repository folder name.")
    parser.add_argument('--first_run', type=bool, required=False, help="Set to True if running for the first time.")
    parser.add_help = True
    args = parser.parse_args()

    repo_url = args.repo_url if args.repo_url else "https://github.com/olinwiol/automation.git"
    git_token = args.git_token if args.git_token else "bb"
    username = args.username if args.username else "olinwiol"
    commit_message = args.commit_message if args.commit_message else "Automated commit message"
    repository = args.repository if args.repository else "automation"
    first_run = args.first_run if args.first_run else False

    initialize_subprocess(git_token, username, commit_message, repository, first_run)
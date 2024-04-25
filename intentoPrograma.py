import re
import subprocess
import logging
from langdetect import detect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_document(file_path):
    try:
        with open(file_path, 'r') as file:
            document_content = file.read()

        # Detect document language
        document_language = detect(document_content)

        # Define regex patterns based on document language
        if document_language == 'en':
            username_pattern = re.compile(r'User(?:s)?:\s*(\w+)', re.IGNORECASE)
            group_pattern = re.compile(r'Group(?:s)?:\s*(\w+)', re.IGNORECASE)
            permission_pattern = re.compile(r'Permission(?:s)?:\s*(\w+)\s+for\s+(User|Group):\s*(\w+)\s+to\s+(read|write|execute)', re.IGNORECASE)
            directory_pattern = re.compile(r'Permissions\s+Directory:\s*(\S+)', re.IGNORECASE)
            file_permission_pattern = re.compile(r'File(?:s)?:\s*(\w+)\s+Permission(?:s)?:\s*(\w+)', re.IGNORECASE)
        elif document_language == 'es':
            username_pattern = re.compile(r'Usuario(?:s)?:\s*(\w+)', re.IGNORECASE)
            group_pattern = re.compile(r'Grupo(?:s)?:\s*(\w+)', re.IGNORECASE)
            permission_pattern = re.compile(r'Permiso(?:s)?:\s*(\w+)\s+para\s+(Usuario|Grupo):\s*(\w+)\s+(?:para\s+)?(leer|escribir|ejecutar)', re.IGNORECASE)
            directory_pattern = re.compile(r'Directorio\s+de\s+Permisos:\s*(\S+)', re.IGNORECASE)
            file_permission_pattern = re.compile(r'Archivo(?:s)?:\s*(\w+)\s+Permiso(?:s)?:\s*(\w+)', re.IGNORECASE)
        elif document_language == 'ca':
            username_pattern = re.compile(r'Usuari(?:s)?:\s*(\w+)', re.IGNORECASE)
            group_pattern = re.compile(r'Grup(?:s)?:\s*(\w+)', re.IGNORECASE)
            permission_pattern = re.compile(r'Permís(?:s)?:\s*(\w+)\s+per\s+a\s+(Usuari|Grup):\s*(\w+)\s+(?:per\s+a\s+)?(llegir|escriure|executar)', re.IGNORECASE)
            directory_pattern = re.compile(r'Directori\s+de\s+Permisos:\s*(\S+)', re.IGNORECASE)
            file_permission_pattern = re.compile(r'Fitxer(?:s)?:\s*(\w+)\s+Permís(?:s)?:\s*(\w+)', re.IGNORECASE)
        else:
            raise ValueError("Unsupported document language")

        # Find all matches
        usernames = [match.group(1) for match in username_pattern.finditer(document_content)]
        groups = [match.group(1) for match in group_pattern.finditer(document_content)]
        permissions = [(match.group(1), match.group(2), match.group(3)) for match in permission_pattern.finditer(document_content)]
        directory_match = directory_pattern.search(document_content)
        permissions_directory = directory_match.group(1) if directory_match else None
        file_permissions = [(match.group(1), match.group(2)) for match in file_permission_pattern.finditer(document_content)]

        return usernames, groups, permissions, permissions_directory, file_permissions
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        raise
    except Exception as e:
        logger.error(f"Error parsing document: {e}")
        raise

def execute_bash_script(script):
    try:
        subprocess.run(script, shell=True, check=True)
        logger.info("Bash script executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing bash script: {e}")
        raise
    except Exception as e:
        logger.error(f"Error executing bash script: {e}")
        raise

def apply_permission(permission, permissions_path):
    try:
        permission_code_map = {'read': 'r', 'write': 'w', 'execute': 'x'}

        target, target_type, permission_type = permission
        permission_code = permission_code_map[permission_type.lower()]

        bash_script = f'chmod {permission_code} {permissions_path}/{target}'

        execute_bash_script(bash_script)
    except Exception as e:
        logger.error(f"Error applying permission '{permission_type}' to '{target}': {e}")
        raise

def main():
    try:
        file_path = input("Enter the path to the document: ")

        usernames, groups, permissions, permissions_directory, file_permissions = parse_document(file_path)

        if permissions_directory is None:
            raise ValueError("Permissions directory not found in the document.")

        for username in usernames:
            apply_permission((username, 'User', 'write'), permissions_directory)

        for group in groups:
            apply_permission((group, 'Group', 'write'), permissions_directory)

        for permission in permissions:
            apply_permission(permission, permissions_directory)

        for file_permission in file_permissions:
            apply_permission(file_permission, permissions_directory)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <unistd.h>

#ifdef _WIN32
#define EOF_KEY_COMBINATION "Ctrl+Z followed by Enter"
#else
#define EOF_KEY_COMBINATION "Ctrl+D"
#endif

#define MAX_FILENAME_LENGTH 50
#define MAX_CONTENT_LENGTH 100
#define MAX_FILES 100
#define MAX_DIRS 100
#define MAX_PATH_COMPONENTS 10
#define MAX_NAME_LENGTH 50

#define READ_PERMISSION 4
#define WRITE_PERMISSION 2
#define EXECUTE_PERMISSION 1

typedef struct {
    char path[MAX_FILENAME_LENGTH * MAX_DIRS];
    char type;
} FoundItem;

typedef struct {
    char name[MAX_FILENAME_LENGTH];
    int size;
    time_t creation_time;
    time_t modified_time;
    char content[MAX_CONTENT_LENGTH];
    int permissions; // Permissions for the file
} File;

typedef struct Directory {
    char name[MAX_FILENAME_LENGTH];
    time_t creation_time;
    File* files[MAX_FILES];
    int file_count;
    struct Directory* subdirs[MAX_DIRS];
    int subdir_count;
    int permissions; // Permissions for the directory
    struct Directory* parent; // Parent directory
} Directory;

Directory* root_directory;
Directory* current_directory;

Directory* create_directory(const char* name, int permissions, Directory* parent) {
    Directory* dir = (Directory*)malloc(sizeof(Directory));
    if (parent == NULL) { // This is the root directory
        strcpy(dir->name, "");
    } else {
        strcpy(dir->name, name);
    }
    dir->creation_time = time(NULL);
    dir->file_count = 0;
    dir->subdir_count = 0;
    dir->permissions = permissions;
    dir->parent = parent;
    return dir;
}

void delete_directory(Directory* dir) {
    for (int i = 0; i < dir->file_count; i++) {
        free(dir->files[i]);
    }
    for (int i = 0; i < dir->subdir_count; i++) {
        delete_directory(dir->subdirs[i]);
    }
    free(dir);
}

File* create_file(const char* name, const char* content, int permissions) {
    File* file = (File*)malloc(sizeof(File));
    strcpy(file->name, name);
    file->size = strlen(content);
    file->creation_time = time(NULL);
    file->modified_time = file->creation_time;
    strcpy(file->content, content);
    file->permissions = permissions;
    return file;
}

File* copy_file(File* file) {
    return create_file(file->name, file->content, file->permissions);
}

void delete_file(File* file) {
    free(file);
}

// void add_file_to_directory(Directory* dir, File* file) {
//     for (int i = 0; i < dir->file_count; i++) {
//         if (strcmp(dir->files[i]->name, file->name) == 0) {
//             printf("File '%s' already exists in the directory.\n", file->name);
//             free(file);
//             return;
//         }
//     }
//     if (dir->file_count < MAX_FILES) {
//         dir->files[dir->file_count++] = file;
//     } else {
//         printf("Directory is full. Cannot add file.\n");
//         free(file);
//     }
// }
void add_file_to_directory(Directory* dir, File* file) {
    for (int i = 0; i < dir->file_count; i++) {
        if (strcmp(dir->files[i]->name, file->name) == 0) {
            printf("File '%s' already exists in the directory.\n", file->name);
            free(file);
            return;
        }
    }
    if (dir->file_count < MAX_FILES) {
        dir->files[dir->file_count++] = file;
    } else {
        printf("Directory is full. Cannot add file.\n");
        free(file);
    }
}

void add_directory_to_directory(Directory* parent_dir, Directory* sub_dir) {
    for (int i = 0; i < parent_dir->subdir_count; i++) {
        if (strcmp(parent_dir->subdirs[i]->name, sub_dir->name) == 0) {
            printf("Directory '%s' already exists in the parent directory.\n", sub_dir->name);
            free(sub_dir);
            return;
        }
    }
    if (parent_dir->subdir_count < MAX_DIRS) {
        parent_dir->subdirs[parent_dir->subdir_count++] = sub_dir;
    } else {
        printf("Parent directory is full. Cannot add sub-directory.\n");
        free(sub_dir);
    }
}
Directory* copy_directory(Directory* dir) {
    Directory* new_dir = create_directory(dir->name, dir->permissions, dir->parent);
    for (int i = 0; i < dir->file_count; i++) {
        add_file_to_directory(new_dir, copy_file(dir->files[i]));
    }
    for (int i = 0; i < dir->subdir_count; i++) {
        add_directory_to_directory(new_dir, copy_directory(dir->subdirs[i]));
    }
    return new_dir;
}
Directory* find_directory_in_directory(Directory* parent_dir, const char* dir_name) {
    for (int i = 0; i < parent_dir->subdir_count; i++) {
        if (strcmp(parent_dir->subdirs[i]->name, dir_name) == 0) {
            return parent_dir->subdirs[i];
        }
    }
    return NULL; // Directory not found
}
void list_directory_contents(Directory* dir, int detailed) {
    printf("Contents of directory '%s':\n", dir->name);
    for (int i = 0; i < dir->file_count; i++) {
        if (detailed) {
            printf("File: %s (Size: %d bytes, Created: %s, Modified: %s, Permissions: %d)\n",
                   dir->files[i]->name, dir->files[i]->size,
                   ctime(&dir->files[i]->creation_time),
                   ctime(&dir->files[i]->modified_time),
                   dir->files[i]->permissions);
        } else {
            printf("%s  ", dir->files[i]->name);
        }
    }
    for (int i = 0; i < dir->subdir_count; i++) {
        if (detailed) {
            printf("Sub-directory: %s (Created: %s, Permissions: %d)\n", dir->subdirs[i]->name,
                   ctime(&dir->subdirs[i]->creation_time),
                   dir->subdirs[i]->permissions);
        } else {
            printf("%s  ", dir->subdirs[i]->name);
        }
    }
}

void delete_file_from_directory(Directory* dir, const char* file_name) {
    int index = -1;
    for (int i = 0; i < dir->file_count; i++) {
        if (strcmp(dir->files[i]->name, file_name) == 0) {
            index = i;
            break;
        }
    }
    if (index >= 0) {
        delete_file(dir->files[index]);
        for (int i = index; i < dir->file_count - 1; i++) {
            dir->files[i] = dir->files[i + 1];
        }
        dir->file_count--;
        printf("File '%s' deleted from directory '%s'.\n", file_name, dir->name);
    } else {
        printf("File '%s' not found in directory '%s'.\n", file_name, dir->name);
    }
}

void delete_subdirectory_from_directory(Directory* dir, const char* sub_dir_name) {
    int index = -1;
    for (int i = 0; i < dir->subdir_count; i++) {
        if (strcmp(dir->subdirs[i]->name, sub_dir_name) == 0) {
            index = i;
            break;
        }
    }
    if (index >= 0) {
        delete_directory(dir->subdirs[index]);
        for (int i = index; i < dir->subdir_count - 1; i++) {
            dir->subdirs[i] = dir->subdirs[i + 1];
        }
        dir->subdir_count--;
        printf("Sub-directory '%s' deleted from directory '%s'.\n", sub_dir_name, dir->name);
    } else {
        printf("Sub-directory '%s' not found in directory '%s'.\n", sub_dir_name, dir->name);
    }
}

void change_file_permissions(File* file, int permissions) {
    file->permissions = permissions;
    printf("File permissions for '%s' changed to %d.\n", file->name, permissions);
}

void change_directory_permissions(Directory* dir, int permissions) {
    dir->permissions = permissions;
    printf("Directory permissions for '%s' changed to %d.\n", dir->name, permissions);
}

void read_file_content(File* file) {
    int user_permissions = (file->permissions / 100) % 10;
    if ((user_permissions & READ_PERMISSION) == 0) {
        printf("Permission denied: You do not have permission to read file '%s'.\n", file->name);
        return;
    }
    printf("Content of file '%s':\n%s\n", file->name, file->content);
}


void change_working_directory(Directory* new_current_directory) {
    current_directory = new_current_directory;
}

void change_to_root_directory() {
    if (root_directory != NULL) {
        current_directory = root_directory;
    } else {
        printf("Root directory not found.\n");
    }
}

void change_to_parent_directory() {
    if (current_directory != root_directory) {
        if (current_directory->parent != NULL) {
            current_directory = current_directory->parent;
        } else {
            printf("Parent directory not found.\n");
        }
    } else {
        printf("Already in root directory.\n");
    }
}

void change_to_subdirectory(const char* sub_dir_name) {
    int index = -1;
    for (int i = 0; i < current_directory->subdir_count; i++) {
        if (strcmp(current_directory->subdirs[i]->name, sub_dir_name) == 0) {
            index = i;
            break;
        }
    }
    if (index >= 0) {
        change_working_directory(current_directory->subdirs[index]);
    } else {
        printf("Sub-directory '%s' not found in current directory.\n", sub_dir_name);
    }
}

void get_directory_path(Directory* dir, char* path) {
    if (dir->parent != NULL) {
        get_directory_path(dir->parent, path);
        if (dir->parent->parent != NULL) { // Not a direct child of root directory
            strcat(path, "/");
        }
        strcat(path, dir->name);
    } else {
        strcat(path, "/");
    }
}

void print_working_directory() {
    char path[MAX_FILENAME_LENGTH * MAX_DIRS] = "";
    get_directory_path(current_directory, path);
    printf("Current working directory: %s\n", path);
}

void append_file_content(File* file) {
    int user_permissions = (file->permissions / 100) % 10;
    if ((user_permissions & WRITE_PERMISSION) == 0) {
        printf("Permission denied: You do not have permission to write to file '%s'.\n", file->name);
        return;
    }
    printf("Current content of file '%s':\n%s\n", file->name, file->content);

    printf("Enter content to append to file '%s' (type %s on a new line to save and exit):\n", file->name, EOF_KEY_COMBINATION);

    char append_content[MAX_CONTENT_LENGTH];
    int c;
    int index = 0;

    // Read the new content from the user
    while ((c = getchar()) != EOF && index < MAX_CONTENT_LENGTH - 1) {
        append_content[index++] = c;
    }

    // Check for Ctrl+D on Unix and Ctrl+Z on Windows to save and exit
    #ifndef _WIN32
    if (c == EOF) {
        printf("Saving changes and exiting...\n");
    }
    #else
    if (c == EOF || c == 26) {
        printf("Saving changes and exiting...\n");
    }
    #endif

    // Add null-terminator at the end of the new content
    append_content[index] = '\0';

    // Clear the input buffer
    while (c != '\n' && c != EOF) {
        c = getchar();
    }

    // Check if appending will exceed the maximum content length
    if (strlen(file->content) + strlen(append_content) < MAX_CONTENT_LENGTH) {
        // Append the new content to the file content
        strcat(file->content, append_content);
        file->size = strlen(file->content);
        file->modified_time = time(NULL);
        printf("Content appended to file '%s'.\n", file->name);
    } else {
        printf("File '%s' is full. Cannot append content.\n", file->name);
    }
}


File* find_file_in_directory(Directory* dir, const char* file_name) {
    for (int i = 0; i < dir->file_count; i++) {
        if (strcmp(dir->files[i]->name, file_name) == 0) {
            return dir->files[i];
        }
    }
    return NULL;
}

Directory* find_subdirectory_in_directory(Directory* dir, const char* sub_dir_name) {
    for (int i = 0; i < dir->subdir_count; i++) {
        if (strcmp(dir->subdirs[i]->name, sub_dir_name) == 0) {
            return dir->subdirs[i];
        }
    }
    return NULL;
}

void display_file_type(const char* file_name) {
    File* file = find_file_in_directory(current_directory, file_name);
    if (file != NULL) {
        printf("File '%s' type: Regular file\n", file_name);
    } else {
        Directory* sub_dir = find_subdirectory_in_directory(current_directory, file_name);
        if (sub_dir != NULL) {
            printf("File '%s' type: Directory\n", file_name);
        } else {
            printf("File '%s' not found in the current directory.\n", file_name);
        }
    }
}

void copy_file_to_directory(Directory* dir, File* file, const char* new_file_name) {
    File* new_file = copy_file(file);
    strcpy(new_file->name, new_file_name);
    add_file_to_directory(dir, new_file);
}

void copy_directory_to_directory(Directory* parent_dir, Directory* sub_dir, const char* new_sub_dir_name) {
    Directory* new_sub_dir = copy_directory(sub_dir);
    strcpy(new_sub_dir->name, new_sub_dir_name);
    add_directory_to_directory(parent_dir, new_sub_dir);
}

void move_file_to_directory(Directory* source_dir, Directory* target_dir, const char* file_name) {
    File* file = find_file_in_directory(source_dir, file_name);
    if (file != NULL) {
        // Check if a file with the same name already exists in the target directory
        File* existing_file = find_file_in_directory(target_dir, file_name);
        if (existing_file != NULL) {
            printf("A file with the name '%s' already exists in the target directory.\n", file_name);
            return;
        }
        // Add the file to the target directory
        target_dir->files[target_dir->file_count++] = file;
        // Remove the file from the source directory
        for (int i = 0; i < source_dir->file_count; i++) {
            if (source_dir->files[i] == file) {
                for (int j = i; j < source_dir->file_count - 1; j++) {
                    source_dir->files[j] = source_dir->files[j + 1];
                }
                source_dir->file_count--;
                break;
            }
        }
        printf("File '%s' moved to directory '%s'.\n", file_name, target_dir->name);
    } else {
        printf("File '%s' not found in source directory.\n", file_name);
    }
}


void move_directory_to_directory(Directory* source_dir, Directory* target_dir, const char* sub_dir_name) {
    Directory* sub_dir = find_subdirectory_in_directory(source_dir, sub_dir_name);
    if (sub_dir != NULL) {
        // Remove the subdirectory from the source directory
        for (int i = 0; i < source_dir->subdir_count; i++) {
            if (source_dir->subdirs[i] == sub_dir) {
                for (int j = i; j < source_dir->subdir_count - 1; j++) {
                    source_dir->subdirs[j] = source_dir->subdirs[j + 1];
                }
                source_dir->subdir_count--;
                break;
            }
        }
        // Add the subdirectory to the target directory
        add_directory_to_directory(target_dir, sub_dir);
        printf("Sub-directory '%s' moved to directory '%s'.\n", sub_dir_name, target_dir->name);
    } else {
        printf("Sub-directory '%s' not found in source directory.\n", sub_dir_name);
    }
}
void parse_path(const char* path, char components[MAX_PATH_COMPONENTS][MAX_NAME_LENGTH]);
void copy_file_or_directory_to_directory(const char* source_name, const char* target_dir_name) {
    // char source_components[MAX_PATH_COMPONENTS][MAX_NAME_LENGTH];
    // parse_path(source_name, source_components);

    if (strchr(source_name, '/') != NULL) {
        printf("Error: Absolute paths or multiple levels of directories are not supported.\n");
        return;
    }
    // Find the source file or directory in the current directory
    File* source_file = find_file_in_directory(current_directory, source_name);
    Directory* source_dir = find_subdirectory_in_directory(current_directory, source_name);

    // Find the target directory in the current directory
    Directory* target_dir = find_subdirectory_in_directory(current_directory, target_dir_name);

    if (source_file != NULL) {
        // Copy the source file to the target directory
        File* copied_file = copy_file(source_file);
        add_file_to_directory(target_dir, copied_file);
    } else if (source_dir != NULL) {
        // Copy the source directory to the target directory
        Directory* copied_dir = copy_directory(source_dir);
        add_directory_to_directory(target_dir, copied_dir);
    } else {
        printf("Source file or directory '%s' not found in the current directory.\n", source_name);
    }
}
void move_file_or_directory_to_directory(const char* source_name, const char* target_dir_name) {
    char source_components[MAX_PATH_COMPONENTS][MAX_NAME_LENGTH];
    parse_path(source_name, source_components);

    if (strchr(source_name, '/') != NULL) {
        printf("Error: Absolute paths or multiple levels of directories are not supported.\n");
        return;
    }
    // Find the source file or directory in the current directory
    File* source_file = find_file_in_directory(current_directory, source_name);
    Directory* source_dir = find_subdirectory_in_directory(current_directory, source_name);

    // Find the target directory in the current directory
    Directory* target_dir = find_subdirectory_in_directory(current_directory, target_dir_name);

    if (source_file != NULL) {
        // Move the source file to the target directory
        move_file_to_directory(current_directory, target_dir, source_name);
    } else if (source_dir != NULL) {
        // Move the source directory to the target directory
        move_directory_to_directory(current_directory, target_dir, source_name);
    } else {
        printf("Source file or directory '%s' not found in the current directory.\n", source_name);
    }
}

void parse_path(const char* path, char components[MAX_PATH_COMPONENTS][MAX_NAME_LENGTH]) {
    int component_index = 0;
    char path_copy[MAX_NAME_LENGTH];
    strncpy(path_copy, path, MAX_NAME_LENGTH);
    char* component = strtok(path_copy, "/");
    while (component != NULL) {
        strncpy(components[component_index++], component, MAX_NAME_LENGTH);
        component = strtok(NULL, "/");
    }
}


void count_lines_words_characters(const char* file_name) {
    File* file = find_file_in_directory(current_directory, file_name);
    if (file != NULL) {
        int lines = 0;
        int words = 0;
        int characters = 0;

        // Count lines, words, and characters
        char* content = file->content;
        int in_word = 0; // Indicates whether we are currently in a word

        while (*content) {
            characters++;
            if (*content == '\n') {
                lines++;
            }

            // Check for the start of a word
            if (*content == ' ' || *content == '\t' || *content == '\n' || *content == '\r' || *content == '\0') {
                in_word = 0;
            } else if (!in_word) {
                in_word = 1;
                words++;
            }

            content++;
        }

        printf("File '%s' statistics:\n", file_name);
        printf("Lines: %d\n", lines);
        printf("Words: %d\n", words);
        printf("Characters: %d\n", characters);
    } else {
        printf("File '%s' not found in the current directory.\n", file_name);
    }
}
void search_pattern_in_file(const char* pattern, const char* file_name) {
    File* file = find_file_in_directory(current_directory, file_name);
    if (file != NULL) {
        printf("Searching for pattern '%s' in file '%s':\n", pattern, file_name);

        char* content = file->content;
        int line_number = 1;

        while (*content) {
            char* line_start = content;
            char* line_end = strchr(content, '\n');
            if (line_end == NULL) {
                line_end = content + strlen(content);
            }

            int line_length = line_end - line_start;
            char line[line_length + 1];
            strncpy(line, line_start, line_length);
            line[line_length] = '\0';

            if (strstr(line, pattern) != NULL) {
                printf("%d: %s\n", line_number, line);
            }

            content = line_end;
            if (*content == '\n') {
                content++; // Move past the newline character
            }
            line_number++;
        }
    } else {
        printf("File '%s' not found in the current directory.\n", file_name);
    }
}

void find_absolute_path(Directory* current_dir, const char* name, char* path, FoundItem* found_items, int* found_count) {
    if (current_dir != NULL) {
        for (int i = 0; i < current_dir->file_count; i++) {
            if (strcmp(current_dir->files[i]->name, name) == 0) {
                found_items[*found_count].type = 'F'; // 'F' for file
                get_directory_path(current_dir, found_items[*found_count].path);
                strcat(found_items[*found_count].path, "/");
                strcat(found_items[*found_count].path, current_dir->files[i]->name);
                (*found_count)++;
            }
        }

        for (int i = 0; i < current_dir->subdir_count; i++) {
            if (strcmp(current_dir->subdirs[i]->name, name) == 0) {
                found_items[*found_count].type = 'D'; // 'D' for directory
                get_directory_path(current_dir->subdirs[i], found_items[*found_count].path);
                strcat(found_items[*found_count].path, "/");
                strcat(found_items[*found_count].path, current_dir->subdirs[i]->name);
                (*found_count)++;
            }
            find_absolute_path(current_dir->subdirs[i], name, path, found_items, found_count);
        }
    }
}

int compare_found_items(const void* a, const void* b) {
    const FoundItem* item_a = (const FoundItem*)a;
    const FoundItem* item_b = (const FoundItem*)b;
    return strcmp(item_a->path, item_b->path);
}


void edit_file(File* file) {
    printf("Current content of file '%s':\n%s\n", file->name, file->content);

    printf("Enter new content for file '%s' (type %s on a new line to save and exit):\n", file->name, EOF_KEY_COMBINATION);

    char new_content[MAX_CONTENT_LENGTH];
    int c;
    int index = 0;

    // Read the new content from the user
    while ((c = getchar()) != EOF && index < MAX_CONTENT_LENGTH - 1) {
        new_content[index++] = c;
    }

    // Check for Ctrl+D on Unix and Ctrl+Z on Windows to save and exit
    #ifndef _WIN32
    if (c == EOF) {
        printf("Saving changes and exiting...\n");
    }
    #else
    if (c == EOF || c == 26) {
        printf("Saving changes and exiting...\n");
    }
    #endif

    // Add null-terminator at the end of the new content
    new_content[index] = '\0';

    // Clear the input buffer
    while (c != '\n' && c != EOF) {
        c = getchar();
    }

    // Update the file content
    strcpy(file->content, new_content);
    file->size = strlen(file->content);
    file->modified_time = time(NULL);

    printf("Content of file '%s' updated.\n", file->name);
}

void show_help() {
    printf("\nList of available commands:\n");
    printf("ls [-l | -la | -al]: List the contents of the current directory.\n");
    printf("mkdir <dir_name> [permissions]: Create a new directory.\n");
    printf("touch <file_name> [permissions]: Create a new file.\n");
    printf("rm <file_name>: Delete a file.\n");
    printf("rmdir <dir_name>: Delete an empty directory.\n");
    printf("cat <file_name>: Display the content of a file.\n");
    printf("chmod <file_or_dir_name> <permissions>: Change permissions of a file or directory.\n");
    printf("cd <dir_name>: Change the current working directory.\n");
    printf("pwd: Print the current working directory.\n");
    printf("append <file_name>: Append content to a file.\n");
    printf("edit <file_name>: Edit the content of a file.\n");
    printf("cp <source_file_or_dir_name> <target_file_or_dir_name>: Copy a file or directory.\n");
    printf("mv <source_file_or_dir_name> <target_file_or_dir_name>: Move a file or directory.\n");
    printf("cpd <source_file_or_dir_name> <target_dir_name>: Copy a file or directory to a directory.\n");
    printf("mvd <source_file_or_dir_name> <target_dir_name>: Move a file or directory to a directory.\n");
    printf("find <name>: Find the absolute path of a file or directory.\n");
    printf("grep <pattern> <file_name>: Search for a pattern in a file.\n");
    printf("help: Display the uses of all commands.\n");
    printf("exit: Exit the program.\n");
}


void execute_command(const char* command) {
    char command_name[MAX_FILENAME_LENGTH];
    char argument1[MAX_FILENAME_LENGTH] = "";
    char argument2[MAX_FILENAME_LENGTH] = "";
    char argument3[MAX_FILENAME_LENGTH] = "";

    sscanf(command, "%s %s %s", command_name, argument1, argument2, argument3);

    if (strcmp(command_name, "ls") == 0) {
        if (strcmp(argument1, "-l") == 0 || strcmp(argument1, "-la") == 0 || strcmp(argument1, "-al") == 0) {
            list_directory_contents(current_directory, 1); // Detailed listing
        } else {
            list_directory_contents(current_directory, 0); // List only names
        }
    } else if (strcmp(command_name, "mkdir") == 0) {
        int permissions = 755; // Default permissions
        if (argument2[0] != '\0') {
            sscanf(argument2, "%d", &permissions);
            if (permissions < 0 || permissions > 777) {
                printf("Invalid permissions. Using default permissions (755).\n");
                permissions = 755;
            }
        }
        Directory* new_dir = create_directory(argument1, permissions, current_directory);
        add_directory_to_directory(current_directory, new_dir);
        if (new_dir->parent == NULL) { // The new directory was not added to the parent directory
            printf("Failed to create directory '%s'.\n", argument1);
        }
    
    } else if (strcmp(command_name, "touch") == 0) {
        int permissions = 644; // Default permissions
        if (argument2[0] != '\0') {
            sscanf(argument2, "%d", &permissions);
            if (permissions < 0 || permissions > 777) {
                printf("Invalid permissions. Using default permissions (644).\n");
                permissions = 644;
            }
        }
        add_file_to_directory(current_directory, create_file(argument1, "", permissions));
    } else if (strcmp(command_name, "rm") == 0) {
        if (argument1[0] != '\0') {
            delete_file_from_directory(current_directory, argument1);
        } else {
            printf("Usage: rm <file_name>\n");
        }
    } else if (strcmp(command_name, "rmdir") == 0) {
        if (argument1[0] != '\0') {
            delete_subdirectory_from_directory(current_directory, argument1);
        } else {
            printf("Usage: rmdir <dir_name>\n");
        }
    } else if (strcmp(command_name, "cat") == 0) {
        if (argument1[0] != '\0') {
            int found_file = 0;
            for (int i = 0; i < current_directory->file_count; i++) {
                if (strcmp(current_directory->files[i]->name, argument1) == 0) {
                    read_file_content(current_directory->files[i]);
                    found_file = 1;
                    break;
                }
            }
            if (!found_file) {
                printf("File '%s' not found in the current directory.\n", argument1);
            }
        } else {
            printf("Usage: cat <file_name>\n");
        }
    } else if (strcmp(command_name, "chmod") == 0) {
        if (argument2[0] != '\0') {
            int permissions;
            sscanf(argument2, "%d", &permissions);
            if (permissions >= 0 && permissions <= 777) {
                // Check if the second argument is a file or directory
                int found_item = 0;
                for (int i = 0; i < current_directory->file_count; i++) {
                    if (strcmp(current_directory->files[i]->name, argument1) == 0) {
                        change_file_permissions(current_directory->files[i], permissions);
                        found_item = 1;
                        break;
                    }
                }
                if (!found_item) {
                    for (int i = 0; i < current_directory->subdir_count; i++) {
                        if (strcmp(current_directory->subdirs[i]->name, argument1) == 0) {
                            change_directory_permissions(current_directory->subdirs[i], permissions);
                            found_item = 1;
                            break;
                        }
                    }
                }
                if (!found_item) {
                    printf("Item '%s' not found in the current directory.\n", argument1);
                }
            } else {
                printf("Invalid permissions. Please enter a number between 0 and 777.\n");
            }
        } else {
            printf("Usage: chmod <file_or_dir_name> <permissions>\n");
        }
    } else if (strcmp(command_name, "cd") == 0) {
        if (strcmp(argument1, "..") == 0) {
            change_to_parent_directory();
        } else if (argument1[0] != '\0') {
            change_to_subdirectory(argument1);
        } else {
            change_to_root_directory();
        }
    } else if (strcmp(command_name, "pwd") == 0) {
        print_working_directory();
    } else if (strcmp(command_name, "append") == 0) {
        if (argument1[0] != '\0') {
            int found_file = 0;
            for (int i = 0; i < current_directory->file_count; i++) {
                if (strcmp(current_directory->files[i]->name, argument1) == 0) {
                    append_file_content(current_directory->files[i]);
                    found_file = 1;
                    break;
                }
            }
            if (!found_file) {
                printf("File '%s' not found in the current directory.\n", argument1);
            }
        } else {
            printf("Usage: append <file_name>\n");
        }

    } else if (strcmp(command_name, "edit") == 0) {
        if (argument1[0] != '\0') {
            int found_file = 0;
            for (int i = 0; i < current_directory->file_count; i++) {
                if (strcmp(current_directory->files[i]->name, argument1) == 0) {
                    read_file_content(current_directory->files[i]);
                    edit_file(current_directory->files[i]);
                    found_file = 1;
                    break;
                }
            }
            if (!found_file) {
                printf("File '%s' not found in the current directory.\n", argument1);
            }
        } else {
            printf("Usage: edit <file_name>\n");
        } 

    } else if (strcmp(command_name, "cp") == 0) {
        if (argument1[0] != '\0' && argument2[0] != '\0') {
            File* file = find_file_in_directory(current_directory, argument1);
            if (file != NULL) {
                copy_file_to_directory(current_directory, file, argument2);
            } else {
                Directory* sub_dir = find_subdirectory_in_directory(current_directory, argument1);
                if (sub_dir != NULL) {
                    copy_directory_to_directory(current_directory, sub_dir, argument2);
                } else {
                    printf("Item '%s' not found in the current directory.\n", argument1);
                }
            }
        } else {
            printf("Usage: cp <source_file_or_dir_name> <target_file_or_dir_name>\n");
        }
    } else if (strcmp(command_name, "mv") == 0) {
        if (argument1[0] != '\0' && argument2[0] != '\0') {
            File* file = find_file_in_directory(current_directory, argument1);
            if (file != NULL) {
                move_file_to_directory(current_directory, current_directory, argument1);
                strcpy(file->name, argument2);
            } else {
                Directory* sub_dir = find_subdirectory_in_directory(current_directory, argument1);
                if (sub_dir != NULL) {
                    move_directory_to_directory(current_directory, current_directory, argument1);
                    strcpy(sub_dir->name, argument2);
                } else {
                    printf("Item '%s' not found in the current directory.\n", argument1);
                }
            }
        } else {
            printf("Usage: mv <source_file_or_dir_name> <target_file_or_dir_name>\n");
        }
    
    } else if (strcmp(command_name, "clear") == 0) {
        #ifdef _WIN32
            system("cls");
        #else
            system("clear");
        #endif

    } else if (strcmp(command_name, "cpd") == 0) {
        if (argument1 != NULL && argument2 != NULL) {
            copy_file_or_directory_to_directory(argument1, argument2);
        } else {
            printf("Usage: cpd <source_file_or_dir_name> <target_dir_name>\n");
        }
    } else if (strcmp(command_name, "mvd") == 0) {
        if (argument1 != NULL && argument2 != NULL) {
            move_file_or_directory_to_directory(argument1, argument2);
        } else {
            printf("Usage: mvd <source_file_or_dir_name> <target_dir_name>\n");
        }
    } else if (strcmp(command_name, "file") == 0) {
        if (argument1[0] != '\0') {
            display_file_type(argument1);
        } else {
            printf("Usage: file <file_name>\n");
        }
    } else if (strcmp(command_name, "wc") == 0) {
        if (argument1[0] != '\0') {
            count_lines_words_characters(argument1);
        } else {
            printf("Usage: wc <file_name>\n");
        }

    } else if (strcmp(command_name, "grep") == 0) {
        if (argument1[0] != '\0' && argument2[0] != '\0') {
            search_pattern_in_file(argument1, argument2);
        } else {
            printf("Usage: grep <pattern> <file_name>\n");
        }

    } else if (strcmp(command_name, "find") == 0) {
        if (argument1[0] != '\0') {
            printf("Finding all occurrences of '%s' in the current directory and its subdirectories:\n", argument1);
            FoundItem found_items[MAX_FILES + MAX_DIRS] = {0};
            int found_count = 0;
            char path[MAX_FILENAME_LENGTH * MAX_DIRS] = "";
            find_absolute_path(current_directory, argument1, path, found_items, &found_count);

            if (found_count == 0) {
                printf("Item '%s' not found in the current directory or its subdirectories.\n", argument1);
            } else {
                // Sort the found items by the absolute path
                qsort(found_items, found_count, sizeof(FoundItem), compare_found_items);

                // Display the results
                for (int i = 0; i < found_count; i++) {
                    char type_symbol = found_items[i].type == 'F' ? 'F' : 'D';
                    printf("%c: %s\n", type_symbol, found_items[i].path);
                }
            }
        } else {
            printf("Usage: find <file_or_dir_name>\n");
        }
    } else if (strcmp(command_name, "help") == 0) {
        show_help();    

    } else if (strcmp(command_name, "exit") == 0) {
        printf("Exiting...\n");
    } else {
        printf("Command not found: %s\nUse 'help' command to know about all command", command_name);
    }
}

int main() {
    root_directory = create_directory("/", 755, NULL);
    current_directory = root_directory;

    char command[MAX_CONTENT_LENGTH];

    do {
        printf("\n%s> ", current_directory->name);
        fgets(command, MAX_CONTENT_LENGTH, stdin);
        command[strcspn(command, "\n")] = '\0'; // Remove the newline character
        execute_command(command);
    } while (strcmp(command, "exit") != 0);

    delete_directory(root_directory);

    return 0;
}

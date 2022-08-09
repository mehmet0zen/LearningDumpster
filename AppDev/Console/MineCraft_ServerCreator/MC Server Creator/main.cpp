//
//  main.cpp
//  MC Server Creator
//
//  Created by Mehmet Yusuf Ozen on 9/22/21.
//

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

#include <sys/stat.h>
#include <stdio.h>
#include <curl/curl.h>

#include "Server_Settings.h"

using namespace std;

//world setting
void WorldSettings() {
    
}

//Command Runner
void RunCommand(string directory) {
    //call a command to run server.jar file
    const string command = "cd \"" + directory + "\"; java -Xmx1024M -Xms1024M -jar server.jar nogui";
    //apply command to terminal
    system(command.c_str());
}

//File installer
void DownloadFiles(string directory){
    
    //install minecraft server to the folder
    const string cmnd = "cd \"" + directory + "\"; curl -H \"Accept: application/zip\" https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar -o server.jar";
    
    //run installin server command
    system(cmnd.c_str());
    
    //run the server command, you should run it twice to accept the terms
    RunCommand(directory);
    
    //create strings to access eula agreement file and edit it to true
    string eula = directory + "/eula.txt";
    string run = directory + "/run.command";

    //ask user if they agree
    string eulaagreed;
    cout << "\n#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\nDo you agree? to continue enter \x1b[33m[true]/[false]\x1b[0m\n\neula=";
    cin >> eulaagreed;
    
    //check if the user really entered a valid answer
    while (eulaagreed != "true" || eulaagreed != "false" || eulaagreed != "TRUE" || eulaagreed != "FALSE") {
        //if user entered true
        if (eulaagreed == "true" || eulaagreed == "TRUE") {
            //open file and agree the eula
            file.open(eula, ios::out);
            if (file.is_open()) {
                file << "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#Thu Sep 23 17:55:42 EDT 2021\neula=true";
                file.close();
                cout << "\n\nEula Agreed\n";
            }
            break;
        }
        
        //if user entered false
        else if (eulaagreed == "false" || eulaagreed == "FALSE") {
            //they didnt accept the eula so tell them how can they accept later on
            cout << "\n\nOH okey.. \x1b[32mif you change your mind just go to [" + eula + "] and change false to true\n\n\x1b[0m";
            exit(0);
        }
        
        //if user entered unidentified word 
        //ask them to enter true or false
        cout << "\n\nyou entered unidentified answer please enter either true or false:";
        cin >> eulaagreed;
    }
    
    //open run or create one and type the code to run server
    file.open(run, ios::out);
    if (file.is_open()) {
        file << "#!/bin/bash\ncd \"$(dirname \"$0\")\"\nexec java -Xms2G -Xmx2G -jar server.jar nogui";
        file.close();
    }

    //ask to user if they want to launch the server
    string launchserver;
    cout << "\n\n||SERVER IS READY||\n\x1b[33mDo you want to run it now?\nyes?[y] - no?[n]\x1b[0m: ";
    cin >> launchserver;

    //while answer is valid [y or n]
    while (launchserver == "y" || launchserver == "n" || launchserver == "Y" || launchserver == "N"){
        // if yes launch the server
        if (launchserver == "y" || launchserver == "Y") {
            RunCommand(directory);
            break;
        } 
        //if no just exit
        else if (launchserver == "n" || launchserver == "N") { 
            cout << "\n\n\nAlright have a nice day!\n\n\n";
            exit(0);
        }
        //if answer isn't valid just ask the question again
        cout << "\n\nThe answer you give: " + launchserver + " isn't a valid answer\nPlease try again [y] or [n]: ";
        cin >> launchserver;
    }
}

//If user wants to run their existing server or create new one
void ExistingOrNew() {
    //Ask user to check if has java oracle and how to install if doesn't
    cout << "\n\n               \x1b[33m||IMPORTANT||\x1b[0m\n\nFirst of all if you don't have Java Oracle you should download those by following one of the links bellow\n\n Java 8 -> https://www.java.com/en/download/\n Java 16 -> https://www.oracle.com/java/technologies/downloads/#java16-mac ##preferred\n\nThese files are needed to launch the server, there is no harm to your computer.\n \x1b[32mIf ready, To continue just hit return [Enter]\x1b[0m";
    //press enter to continue
    cin.get();
    
    //ask if user has already created a server
    cout << "\n\nAlready created a server with this app? run it by entering \x1b[31m[R]\x1b[0m\nDon't have a server? enter \x1b[31m[N]\x1b[0m to create new one!\n --> ";

    //Get the answer
    string answerRN, directory;
    cin >> answerRN;

    while (answerRN != "R" || answerRN != "N") {
        //if R run the server in directory
        if (answerRN == "R") {
            cout << "\nwhere is your server folder located?\nfind and drag it in here! \n(you can also copy paste the file path)\n path: ";

            cin.ignore();
            getline(cin ,directory);

            cout << "Running your server...\n\n";
            //Run command
            RunCommand(directory);
            //exit
            exit(0);
        } else if (answerRN == "N") {
            cout << "\nAlright we would like you to answer couple of questions first...";
            break;
        } else {
            cout << "oops! entered [" << answerRN << "] is not in our options\n sorry for the confusion please try again \n enter \x1b[31m[R]\x1b[0m to run an existing server\n or enter \x1b[31m[N]\x1b[0m to create a new server: ";
            cin >> answerRN;
        }
    }
}

//Creating Folder
void CreateServer() {
    ExistingOrNew();

    //Creating the folder
    //server_name variable
    string folder_name;
    
    //ask for the server name
    cout << "\n\n\nIf you want to skip any of the questions you can simply enter \x1b[31m[D]\x1b[0m as Default\n\n";
    cout << "File name default [D]: \x1b[32m[minecraft_server]\x1b[0m\nEnter folder name: ";
    cin.ignore();
    getline(cin, folder_name);
    cout << "\n\n";
    
    //Server default name
    if (folder_name == "D") {
        folder_name = "minecraft_server";
    }

    //create home direction
    const string homeDir = getenv("HOME");

    //direction for the folder
    string folderDir, finalDir;
    
    //Folder direction
    cout << "Default location [D]: \x1b[32m[" << homeDir + "/Desktop" << "]\x1b[0m (you can drag and drop the folder) //DONT USE SPACES//\n";
    cout << "location for the folder: ";
    cin >> folderDir;
    
    //folder default name
    if (folderDir == "D") {
        folderDir = homeDir + "/Desktop";
    }
    finalDir = folderDir + "/" + folder_name;
    cout << finalDir;

    int extra = 1;
    string answer;
    //if in that direction there is already a folder exists in that name ask if the person wants to run or create a new one
    if (mkdir(finalDir.c_str(), 0775)) {
        cout << "\n\n\n\x1b[32mFolder named\x1b[0m \x1b[34m[" + folder_name + "]\x1b[0m \x1b[32malready exists would you like to run it? or create new one?\x1b[0m\n[R] / [N]\n--> ";
        cin >> answer;
        cout << "\n\n";

        while (answer != "R" || answer != "N") {
            if (answer == "R") {
                cout << "Running your server...\n\n";
                RunCommand(finalDir);
                exit(0);
            } else if (answer == "N"){
                while (mkdir(string(finalDir + to_string(extra)).c_str(), 0775)) {
                    extra += 1;
                }
                finalDir += to_string(extra);
                break;
            }
            cout << "\n\nSorry but you should enter \x1b[32m[R]\x1b[0m to run or \x1b[32m[N]\x1b[0m to create a new project\n--> ";
            cin >> answer;
        }

    } else {
        mkdir(finalDir.c_str(), 0775);
    }
    //Feedback
    cout << "\nFolder Created -- " << finalDir << "\n";
    
    cout << "\n\n" << finalDir << "\n\n\n";
    
    //downloading server.jar file
    DownloadFiles(finalDir);
    
}

int main ()
{
    CreateServer();
    return 0;
}

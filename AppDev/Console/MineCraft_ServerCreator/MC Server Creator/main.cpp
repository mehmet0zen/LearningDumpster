#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

#include <sys/stat.h>
#include <stdio.h>
#include <curl/curl.h>
#include "Server_Settings.h"

using namespace std;

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
    string eulaFile = directory + "/eula.txt";
    string runFile = directory + "/run.command";

    //check if the user really entered a valid answer

        if (eulaAgreed) {
            //open file and agree the eula
            file.open(eulaFile, ios::out);
            if (file.is_open()) {
                file << "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#Thu Sep 23 17:55:42 EDT 2021\neula=true";
                file.close();
                cout << "\n\nEula Agreed\n";
            }
        }

        //if user entered false
        else if (!eulaAgreed) {
            //they didnt accept the eula so tell them how can they accept later on
            //GIVE WARNING
        }

    //open run or create one and type the code to run server
    file.open(runFile, ios::out);
    if (file.is_open()) {
        file << "#!/bin/bash\ncd \"$(dirname \"$0\")\"\nexec java -Xms2G -Xmx2G -jar server.jar nogui";
        file.close();
    }
}

//Creating Server
void CreateServer() {
    //Creating the folder
    string folderDir = folderDirection;
    //Folder direction
    cout << folderDirection;


    int extra = 1;
    //if in that direction there is already a folder exists in that name ask if the person wants to run or create a new one
    if (mkdir(folderDir.c_str(), 0775)) {
        while (mkdir(string(folderDir + to_string(extra)).c_str(), 0775)) {
            extra += 1;
        }
        folderDir += to_string(extra);
    } else {
        mkdir(folderDir.c_str(), 0775);
    }

    //Feedback
    cout << "\nFolder Created -- " << folderDir << "\n";

    //downloading server.jar file
    DownloadFiles(folderDir);

}

int main(int argc, char *argv[])
{
    CreateServer();
    return 0;
}

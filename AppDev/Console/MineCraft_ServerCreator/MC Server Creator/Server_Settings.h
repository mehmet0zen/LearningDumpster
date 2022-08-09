//
//  Server_Settings.h
//  MC Server Creator
//
//  Created by Mehmet Yusuf Ozen on 9/24/21.
//
#include <string>
using namespace std;
#pragma once


fstream file;
string serverName = "A minecraft server";
//Gamemode: survival, hardcore, creative [survival]
//If hardcore difficulty will be hard, cheats and bonus chests will be off.
//If creative cheats default will be on.
string gameMode = "survival";
//Difficulty: peaceful, easy, normal, hard [normal]
string defficulty = "normal";
string allowCheats = "off";


//broadcast-rcon-to-ops=true
//view-distance=10
//enable-jmx-monitoring=false
//server-ip=
//resource-pack-prompt=
//rcon.port=25575
//gamemode=survival
//server-port=25565
//allow-nether=true
//enable-command-block=false
//enable-rcon=false
//sync-chunk-writes=true
//enable-query=false
//op-permission-level=4
//prevent-proxy-connections=false
//resource-pack=
//entity-broadcast-range-percentage=100
//level-name=world
//rcon.password=
//player-idle-timeout=0
//motd=A Minecraft Server
//query.port=25565
//force-gamemode=false
//rate-limit=0
//hardcore=false
//white-list=false
//broadcast-console-to-ops=true
//pvp=true
//spawn-npcs=true
//spawn-animals=true
//snooper-enabled=true
//difficulty=easy
//function-permission-level=2
//network-compression-threshold=256
//text-filtering-config=
//require-resource-pack=false
//spawn-monsters=true
//max-tick-time=60000
//enforce-whitelist=false
//use-native-transport=true
//max-players=20
//resource-pack-sha1=
//spawn-protection=16
//online-mode=true
//enable-status=true
//allow-flight=false
//max-world-size=29999984
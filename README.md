# GetGud Python SDK


Getgud Python SDK allows you to integrate your game with the GetGud platform. Once integrated, you will be able to stream your matches to Getgud's cloud, as well as to send reports and update player's data.

## Table of Contents

- [Prerequsites](https://github.com/getgud-io/cpp-getgud-sdk#prerequisites)
- [How SDK works](https://github.com/getgud-io/cpp-getgud-sdk#how-sdk-works)
- [Getting Started](https://github.com/getgud-io/cpp-getgud-sdk#getting-started)
- [Configuration](https://github.com/getgud-io/cpp-getgud-sdk#configuration)
    - [Description of the Config fields](https://github.com/getgud-io/cpp-getgud-sdk#description-of-the-config-fields)
- [Logging](https://github.com/getgud-io/cpp-getgud-sdk#logging)
- [Usage](https://github.com/getgud-io/cpp-getgud-sdk#usage)
    - [Initialization](https://github.com/getgud-io/cpp-getgud-sdk#initialization)
    - [Starting Games and Matches](https://github.com/getgud-io/cpp-getgud-sdk#starting-games-and-matches)
    - [Adding Actions to live Match](https://github.com/getgud-io/cpp-getgud-sdk#adding-actions-to-live-match)
    - [Adding Chat messages and Reports to live Match](https://github.com/getgud-io/cpp-getgud-sdk#adding-chat-and-reports-to-live-match)
    - [Ending Games and Matches](https://github.com/getgud-io/cpp-getgud-sdk#ending-games-and-matches)
    - [Sending Reports to past Matches](https://github.com/getgud-io/cpp-getgud-sdk#sending-reports-to-finished-matches)
    - [Sending Player Updates](https://github.com/getgud-io/cpp-getgud-sdk#sending-player-updates)
    - [Disposing the SDK](https://github.com/getgud-io/cpp-getgud-sdk#disposing-the-sdk)
- [Examples](https://github.com/getgud-io/cpp-getgud-sdk#examples)

## Prerequisites

To start, let’s talk about the logical structure of how Getgud is built.

`Title->1->N->Game->1->N->Match`


* The top container in Getgud's SDK is `Title`, which represents a literal game’s title, you as a client can have many titles, for example, a `Title` named CS:GO represents the CS:GO video game.  Title holds an Id, PII, permissions, etc. 

  ```
  Example of Title: CS:GO 
  ```

* Next up is `Game`, it is a container of matches that belong to the same `Title` from the same server session, where mostly the same players in the same teams, play one or more `Matches` together. You as a client can identify every game with a unique `gameGuid` that is given to you when the `Game` starts. 

  ```
  An example of a Game is a CS:GO Game which has 30 macthes (AKA rounds) inside it.
  ```

* `Match` represents the actual play time that is streamed for analysis.  Like `Game`, `Match` also has a GUID which will be provided to you once you start a new match

  ```
  An example of a Match is a single CS:GO round inside the game.
  ```

* The `Player` entity represents a literal player and holds the player’s PII. A Player belongs to a `Title`. Player also has a GUID, which should be unique to the `titleId`. A player has an interesting relationship with `Match`, it’s a N:N relationship; a match holds many players and a player plays in many matches.

* A `TB Type` (AKA toxic behavior type) and its child `TB Subtype` are entities that represent toxic behaviors (cheating as well as griefing). For example, one TB-Type might represent the Aimbot cheat and one of its child TB-Subtypes would be Spinbot. You are going to use this when sending your `Reports` to Getgud.

## How SDK works

To effectively control the SDK it is important to understand how it works behind the scenes. 

![plot](./img/getgud_schema.png)

In the graph, we show a high-level idea of what happens when you call any of the SDK commands. The functionality of SDK can be divided into 3 main components which are completely separated from one another.
- Sending live Game Data (Actions, Reports, Chat for live Matches)
- Send Reports for finished Games
- Send Player Update events

Each of those 3 components has a similar structure to what we showed on the graph. 
When you call the command in Getgud SDK the command is then passed to the "Buffer" and one of the Sender threads on the other side picks the command and accumulates it forming the JSON packets that will be at some time point sent to Getgud.

Sending live Game Data is a much more consuming process than Sending Reports and Players, there will be not many events you will send to us, unlike sending live Game Data. With live Game Data, you will send us THOUSANDS of updates per tick. That is why we allow to spawn more than 1 sender only for sending Live Game data, you will see this reflected in the config file.

## Getting Started

To use the GetGud SDK, you will need to include the required header file:

```cpp
#include "../include/GetGudSdk.h"
```

First things first, you need to Init SDK in your code. To do this type:

```cpp
GetGudSdk::Init();
```

This will load the default Config and set up SDK for working. Note that to customize how SDK works you will need to use your own `config.json` file.

Next, you need to start a Game, you can do it like this:

```cpp
std::string gameGuid = GetGudSdk::StartGame(
  1, //titleId
  "6a3d1732-8f72-12eb-bdef-56d89392f384", //privateKey
  "us-west-1", // serverGuid
  "deathmatch" // gameMode
);
```

Once the Game is started you get the Game guid and you can start the Match using your gameGuid.

```cpp
std::string matchGuid = GetGudSdk::StartMatch(
  gameGuid, 
  "deathmatch", // matchMode
  "de-dust" // mapName
);
```

When you start the Match you get its matchGuid. Now you can push Action, Chat Data, and Reports to the Match. Let's push a Spawn Action to this match.

```cpp
bool isActionSent = GetGudSdk::SendSpawnAction(
          matchGuid,
          1684059337532,  // actionTimeEpoch
          "player_1", // playerGuid
          "ttr", // characterGuid
          GetGudSdk::PositionF{1, 2, 3}, // position
          GetGudSdk::RotationF{10, 20} // rotation
);
```

Let's also create one more match and push a report.

```cpp
std::string matchGuid = GetGudSdk::StartMatch(
  gameGuid, 
  "deathmatch", // matchMode
  "de-mirage" // mapName
);

GetGudSdk::ReportInfo reportInfo;
reportInfo.MatchGuid = "6a3d1732-8f72-12eb-bdef-56d89392f384";
reportInfo.ReportedTimeEpoch = 1684059337532;
reportInfo.ReporterName = "player1";
reportInfo.ReporterSubType = 0;
reportInfo.ReporterType = 0;
reportInfo.SuggestedToxicityScore = 100;
reportInfo.SuspectedPlayerGuid = "player1";
reportInfo.TbSubType = 0;
reportInfo.TbTimeEpoch = 1684059337532;
reportInfo.TbType = 0;
GetGudSdk::SendInMatchReport(reportInfo);

```

Great, it is time to stop the Game now. To do it just specify what Game you need to stop, all the Matches inside this Game will be stopped automatically.

```cpp
bool gameEnded = GetGudSdk::MarkEndGame(gameGuid);
```

In the end, just dispose SDK when you do not need it anymore.

```cpp
GetGudSdk::Dispose();
```

## Configuration

The Config JSON file is loaded during `GetGudSdk::Init();` operation using `CONFIG_PATH` env variable.
Example of configuration file `config.json`:

```json
{
  "streamGameURL": "http://44.204.78.198:3000/api/game_stream/send_game_packet",
  "updatePlayersURL": "http://44.204.78.198:3000/api/player_data/update_players",
  "sendReportsURL": "http://44.204.78.198:3000/api/report_data/send_reports",
  "throttleCheckUrl": "http://44.204.78.198:3000/api/game_stream/throttle_match_check",
  "logToFile": true,
  "logFileSizeInBytes": 2000000,
  "circularLogFile": true,
  "reportsMaxBufferSizeInBytes": 100000,
  "maxReportsToSendAtOnce": 100,
  "maxChatMessagesToSendAtOnce": 100,
  "playersMaxBufferSizeInBytes": 100000,
  "maxPlayerUpdatesToSendAtOnce": 100,
  "gameSenderSleepIntervalMilliseconds": 100,
  "apiTimeoutMilliseconds": 600,
  "apiWaitTimeMilliseconds": 100,
  "packetMaxSizeInBytes": 2000000,
  "actionsBufferMaxSizeInBytes": 10000000,
  "gameContainerMaxSizeInBytes": 50000000,
  "maxGames": 25,
  "maxMatchesPerGame": 10,
  "minPacketSizeForSendingInBytes": 1000000,
  "packetTimeoutInMilliseconds": 100000,
  "gameCloseGraceAfterMarkEndInMilliseconds": 20000,
  "liveGameTimeoutInMilliseconds": 100000,
  "hyperModeFeatureEnabled": true,
  "hyperModeMaxThreads": 10,
  "hyperModeAtBufferPercentage": 10,
  "hyperModeUpperPercentageBound": 90,
  "hyperModeThreadCreationStaggerMilliseconds": 100,
  "logLevel": "FULL"
}
```

Please note that SDK will not start if `CONFIG_PATH` is not set.
Make sure to adjust the values in the configuration file according to your application's requirements.

### Description of the Config fields

#### General API connection fields
- `streamGameURL`: The link to Getgud API which will be used to send actions, chat, and reports for live matches.
- `updatePlayersURL`: The link to Getgud API which will be used to send Player Update events to Getgud.
- `sendReportsURL`: The link to Getgud API which will be used to send Reports for finished Matches.
- `throttleCheckUrl`: The link to Getgud API which will be used to throttle check each match before sending its actions, reports, and chat to us. It is a way for Getgud to tell SDK if this match is interesting for it or not.
- `logLevel`: Log level setting, in other words, how much you want to log into the log file. 
  - `FULL`: Log everything
  - `WARN_AND_ERROR`: Log all errors and warnings
  - `_ERROR`: Log all errors
  - `FATAL`: Log only fatal errors

- `logToFile`: Weather SDK should write the logs to file or no
- `logFileSizeInBytes`: Maximum log file size in bytes `(0, 100000000)` bytes
- `circularLogFile`: In case this is set to true and the log file size exceeds the limit the SDK will start removing the first lines of the file to push more logs to the end of the log file

#### Offline Report Sending fields
- `reportsMaxBufferSizeInBytes`: Maximum size of the reports buffer in bytes for sending reports for finished matches. If the size of Report buffer fills too quickly all the next reports you send to us will be disregarded. `(0, 10000000)` bytes.
- `maxReportsToSendAtOnce`: Maximum number of reports for offline matches that will be sent to Getgud at once. `(0, 100)` reports.

#### Player Update fields
- `playersMaxBufferSizeInBytes`: Maximum size of the player updates buffer in bytes for sending player updates. If the size of Player Update buffer fills too quickly all the next player updates you send to us will be disregarded. `(0, 10000000)` bytes.
- `maxPlayerUpdatesToSendAtOnce`: Maximum number of player updates that will be sent to Getgud at once. `(0, 100)` reports.

#### Chat messages
- `maxChatMessagesToSendAtOnce`: Maximum amount of chat messages to send at once with game packet. `(0,100)` chat messages.


#### Live Games and Matches fields
- `gameSenderSleepIntervalMilliseconds`: Sleep time of every Game Sender. `(0, 5000)` milliseconds.
- `apiTimeoutMilliseconds`: API timeout in milliseconds, the maximum time the data transfer is allowed to complete. `(0, 20000)` milliseconds.
- `apiWaitTimeMilliseconds`: The SDK will be trying to send the game packet for this time frame. So it will do K attempts to send the packet, each attempt will have a timeout of `apiTimeoutMilliseconds`, and when it fails it will try to send again until the wait time is over. `(0, 20000)` milliseconds.
- `packetMaxSizeInBytes`: Maximum size of a game packet in bytes to send to Getgud. `(0, 2000000)` bytes.
- `actionsBufferMaxSizeInBytes`: Maximum size of the actions buffer in bytes. We use Action Buffer to transfer actions from GetGudSdk to one of the Game Senders. `(500, 100000000)` bytes.
- `gameContainerMaxSizeInBytes`: Maximum size of the game container in bytes. We use Game Container to transfer metadata of Games and Matches to one of the Game Senders. `(500, 500000000)` bytes.
- `maxGames`: Maximum number of live Games allowed at once. `(1, 100)` games.
- `maxMatchesPerGame`: Maximum number of live Matches per live Game. `(1, 100)` matches.
- `minPacketSizeForSendingInBytes`: Minimum size of a packet required for sending to Getgud in bytes. `(500, 1500000)` bytes.
- `packetTimeoutInMilliseconds`: If a live Game is not getting any action in this time frame, the game packet to Getgud will be sent even though its size is less than `minPacketSizeForSendingInBytes`. `(500, 100000)` milliseconds.
- `gameCloseGraceAfterMarkEndInMilliseconds`: Grace period in milliseconds after marking a game as ended before closing it. This is done to accumulate some actions which may still not be in the game packet. `(0, 200000)` milliseconds.
- `liveGameTimeoutInMilliseconds`: If the live game didn't receive any actions for this time in milliseconds we will close it. `(0, 300000)` milliseconds.
- `hyperModeFeatureEnabled`: Flag to enable or disable the hypermode feature. Hyper mode allows spawning more than 1 Game Sender thread in case the Action Buffer or Game Container becomes too large. `true, false`
- `hyperModeMaxThreads`: Maximum number of threads allowed in hypermode. In other words how many Game Senders can we have active. `(1, 20)` threads.
- `hyperModeAtBufferPercentage`: Percentage of buffer usage to trigger hypermode. If action buffer or game container usage is larger than this %, SDK will start spawning extra threads. `(10, 90)` %.
- `hyperModeUpperPercentageBound`: Upper percentage bound for buffer usage in hypermode, at this % usage SDK will have `hyperModeMaxThreads` activated. `(30, 90)` %.
- `hyperModeThreadCreationStaggerMilliseconds`: Time interval between the creation of consecutive threads (Game senders) in hypermode in milliseconds. `(0, 10000)` milliseconds.

## Logging

SDK will log all its actions depending on what `logLevel` you set up in the config file. You should also set up env variable `LOG_FILE_PATH` with the path to the file where SDK will log data, otherwise, the logging will not work.

In order to control how you log use the following config parameters:
```json
"logToFile": true,
"logFileSizeInBytes": 2000000,
"circularLogFile": true,
```

This will allow you to control how much you log and what to do if the log file exceeds the memory limit.
# GetGud Python SDK


Getgud Python SDK allows you to integrate your game with the GetGud platform. Once integrated, you will be able to stream your matches to Getgud's cloud, as well as to send reports and update player's data.

All our SDKs including C and Python SDKs are based on the C++ SDK, for complete documentation you can visit our [C++ SDK page](https://github.com/getgud-io/cpp-getgud-sdk)

## Table of Contents
- [Downloads](https://github.com/getgud-io/python-getgud-sdk#downloads)
- [Getting Started](https://github.com/getgud-io/python-getgud-sdk#getting-started)
- [Configuration](https://github.com/getgud-io/python-getgud-sdk#configuration)
    - [Description of the Config fields](https://github.com/getgud-io/python-getgud-sdk#description-of-the-config-fields)
- [Logging](https://github.com/getgud-io/python-getgud-sdk#logging)

## Downloads

[Linux latest build](https://getgud-sdk-files.s3.amazonaws.com/0.1.0-Alpha-230531-b3ec5a8/Linux/libGetGudSdk.so) <br>
[Windows latest build](https://getgud-sdk-files.s3.amazonaws.com/0.1.0-Alpha-230531-b3ec5a8/Linux/libGetGudSdk.so)

## Getting Started

To use our SDK in python you will have to build it for your system first. In order to do this just follow this simple steps.

1. If you do not have Python environment and start from scratch you can install Miniconda.

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.3.1-0-Linux-x86_64.sh
bash Miniconda3-py39_23.3.1-0-Linux-x86_64.sh
source miniconda3/bin/activate
conda create -n getgudsdk python=3.9 anaconda
conda activate getgudsdk
pip install -r requirements.txt
```

For windows to install Miniconda visit [this link](https://docs.conda.io/en/latest/miniconda.html)
Now let's build the SDK!

2. First download the latest Windows/Linux library build files from our S3 bucket

3. Run the command in your terminal to build the library
```bash
invoke build-sdk
export LD_LIBRARY_PATH=$PWD/python-getgud-sdk:$LD_LIBRARY_PATH
```

4. Do not forget to set `LOG_FILE_PATH` and `CONFIG_PATH` environment variables to use SDK!

We have build the SDK an it is ready for use!

First, you will need to import `GetGudSdk` from the Python wrapper:

```python
from getgudsdk_wrapper import GetGudSdk
import time
import random
```

Initialize the SDK:

```python
sdk = GetGudSdk()
```

Next, start a Game:

```python
game_guid = sdk.start_game(1, "private_key", "server_guid", "game_mode")
```

Once the Game has started, you can start a Match using `game_guid`:

```python
match_guid = sdk.start_match(game_guid, "match_mode", "map_name")
```

Now you can push Actions, Chat Data, and Reports to the Match. Let's push a Spawn Action to this match:

```python
action_time_epoch = int(time.time() * 1000)
player_guid = "player_1"
character_guid = "ttr"
position = (1, 2, 3)
rotation = (10, 20, 30)
team_id = 1
initial_health = 100

sdk.send_spawn_action(match_guid, action_time_epoch, player_guid, character_guid, team_id, initial_health, position, rotation)
```

Let's also create one more match and push a report:

```python
match_guid = sdk.start_match(game_guid, "deathmatch", "de-mirage")

reporter_name = "player1"
reporter_type = 0
reporter_sub_type = 0
suspected_player_guid = "player1"
tb_type = 0
tb_sub_type = 0
tb_time_epoch = int(time.time() * 1000)
suggested_toxicity_score = 100
reported_time_epoch = int(time.time() * 1000)

sdk.send_in_match_report(match_guid, reporter_name, reporter_type, reporter_sub_type, 
                         suspected_player_guid, tb_type, tb_sub_type, 
                         tb_time_epoch, suggested_toxicity_score, reported_time_epoch)
```

It's time to stop the Game now. To do this, just specify which Game you need to stop, and all the Matches inside this Game will be stopped automatically:

```python
sdk.mark_end_game(game_guid)
```

Finally, dispose of the SDK when you no longer need it:

```python
sdk.dispose()
```

## Configuration

The Config JSON file is loaded during `init()` operation using `CONFIG_PATH` env variable.
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

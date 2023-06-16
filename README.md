# GetGud Python SDK

## What Can You Do With GetGud's SDK

Getgud Python SDK allows you to integrate your game with the GetGud platform. Once integrated, you will be able to:
- Stream live Game data to GetGud's cloud (In-match Actions, In-match Reports, In-match Chat messages)
- Send Reports about historical matches to GetGud.
- Send (and update) player information to GetGud.

## Prerequisites

To start, we should understand the basic structure Getgud's SDK uses to understand an FPS: 

**Titles->1->N->Games->1->N->Matches->1->N->Actions**

* The top container in Getgud's SDK is `Title`, which represents a literal game’s title, you as a client can have many titles, for example, a `Title` named CS:GO represents the CS:GO video game.

  ```
  An example of a Title: CS:GO 
  ```

* Next up is `Game`, a `Game` is a container of matches that belong to the same `Title` from the same server session, where mostly the same players in the same teams, play one or more `Matches` together. You as a client can identify every game with a unique `gameGuid` that is provided to you once the `Game` starts. 

  ```
  An example of a Game is a CS:GO game which has 30 macthes (AKA rounds) inside it.
  ```

* `Match` represents the actual play time that is streamed for analysis.
A `Match` is the containr of actions that occured in the match's timespan.
Like `Game`, `Match` also has a GUID which will be provided to you once you start a new match.

  ```
  An example of a Match is a single CS:GO round inside the game.
  ```

* `Action` represents an in-match activity that is associated with a player. We collect six different action types which are common to all first person shooter gamnes:
1. `Spwan` - Whenever a player appears or reappears in-match, on the map.
2. `Death` - A death of a player.
3. `Position` - player position change (including looking direction).
4. `Attack` - Whenever a player initiates any action that might cause damage, now or in the future. Examples: shooting, throwning a granade, planting a bomb, swinging a sword, punching, firing a photon torpedo, etc.
5. `Damage` - Whenever a player recieves any damage, from players or the environment.
6. `Heal` - Whenever a player is healed.


## Getting Started

First, you need to build the SDK for your system. Follow these steps:

1. Install Miniconda by executing the following commands:

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.3.1-0-Linux-x86_64.sh
   bash Miniconda3-py39_23.3.1-0-Linux-x86_64.sh
   source miniconda3/bin/activate
   conda create -n getgudsdk python=3.9 anaconda
   conda activate getgudsdk
   pip install -r requirements.txt
   ```

   For Windows, you can download Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html).

2. Download the latest Windows or Linux library build files from GetGud's S3 bucket.

3. Run the following command in your terminal to build the library:

   ```bash
   invoke build-sdk
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/your/python-getgud-sdk
   ```

   On Windows, add the path to the SDK .pyd file to PYTHONPATH.

4. Set the `LOG_FILE_PATH` and `CONFIG_PATH` environment variables to use the SDK.

Now let's get started with the SDK!

To use the GetGud Python SDK, you need to import the `GetGudSdk` class and other necessary modules:

```python
from getgudsdk_wrapper import GetGudSdk
import time
import random
```

Initialize the SDK:

```python
sdk = GetGudSdk()
```

Start a Game:

```python
game_guid = sdk.start_game(1, "private_key", "server_guid", "game_mode")
```

Once the Game starts, you can start a Match:

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

Create one more match and push a report:

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

Stop the Game:

```python
sdk.mark_end_game(game_guid)
```

Finally, dispose of the SDK when you no longer need it:

```python
sdk.dispose()
```

## SDK Methods

### start_game

Starts a new game and returns the `gameGuid`, a unique identifier for the game.

Parameters:
- `title_id` - The title ID provided by GetGud.io.
- `private_key` (str) - The private key associated with the title ID.
- `server_name` (str) - A unique name for your game server.
- `game_mode` (str) - The mode of the game.

Returns:
- `game_guid` (str) - The unique identifier for the game.

### start_match

Starts a new match within a game and returns the `matchGuid`, a unique identifier for the match.

Parameters:
- `game_guid` (str) - The unique identifier for the game.
- `match_mode` (str) - The mode of the match.
- `map_name` (str) - The name of the map for the match.

Returns:
- `match_guid` (str) - The unique identifier for the match.

### send_action

Sends an action to a match. Actions can include spawn, position, attack, damage, heal, and death.

Parameters:
- `match_guid` (str) - The unique identifier for the match.
- `action` (dict) - The action data.

### mark_end_game

Marks a game as ended. This will close the game on the GetGud platform.

Parameters:
- `game_guid` (str) - The unique identifier for the game.

Returns:
- `game_ended` (bool) - Whether the game was successfully closed or not.

### send_chat_message

Sends a chat message to a match.

Parameters:
- `match_guid` (str) - The unique identifier for the match.
- `message_data` (dict) - The chat message data.

### send_in_match_report

Sends a report for a match.

Parameters:
- `match_guid` (str) - The unique identifier for the match.
- `report_info` (dict) - The report information.

### update_players

Updates player information.

Parameters:
- `title_id` (int) - The title ID provided by GetGud.io (optional if using environment variables).
- `private_key` (str) - The private key associated with the title ID (optional if using environment variables).
- `player_infos` (list) - A list of player information dictionaries to update.

Returns:
- `players_updated` (bool) - Whether the player information was successfully updated or not.

### dispose

Disposes of the SDK when no longer needed.



## Configuration

The Config JSON file is loaded during initialization using the `CONFIG_PATH` environment variable.
Example of configuration file `config.json`:

```json
{
  "streamGameURL": "http://44.204.78.198:3000/api/game_stream/send_game_packet",
  "updatePlayersURL": "http://44.204.78.198:3000/api/player_data/update_players",
  "sendReportsURL": "http://44.204.78.198:3000/api/report_data/send_reports",
  "throttleCheckUrl": "http://44.204.78.198:3000/api/game_stream/throttle_match_check",
  "logLevel": "FULL"
}
```

Please note that the SDK will not start if `CONFIG_PATH` is not set. Adjust the values in the configuration file according to your application's requirements.

## Logging

The SDK logs its actions based on the `logLevel` setting in the configuration file. Logging will only work if the `LOG_FILE_PATH` environment variable is set.

To control logging, use the following configuration parameters:

- `logToFile`: true/false - Whether to log to a file or not.
- `logFileSizeInBytes`: Maximum log file size in bytes (0-100000000).
- `circularLogFile`: true/false - Whether to remove the first lines of the log file when it exceeds the size limit.

Please make sure to set the `LOG_FILE_PATH` and `CONFIG_PATH` environment variables correctly to use logging.

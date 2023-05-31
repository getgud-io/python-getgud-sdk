from getgudsdk_wrapper import GetGudSdk
import time

if __name__ == "__main__":
    sdk = GetGudSdk()
    game_guid = sdk.start_game("pk", "aws", "deathmatch")
    print(game_guid)
    match_guid = sdk.start_match(game_guid, "test_map", "deathmatch")
    print(match_guid)
    sdk.dispose()
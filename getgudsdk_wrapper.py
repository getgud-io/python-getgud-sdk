import getgudsdk.lib as getgudsdk
from getgudsdk import ffi
import time

class GetGudSdk:
    def __init__(self):
        getgudsdk.init()

    def start_game(self, title_id, private_key, server_guid, game_mode):
        game_info = ffi.new("struct StartGameInfo*")
        game_info.titleId = title_id

        game_info.privateKey = ffi.new("char[]", private_key.encode('utf-8'))
        game_info.privateKeySize = len(private_key)
        
        game_info.serverGuid = ffi.new("char[]", server_guid.encode('utf-8'))
        game_info.serverGuidSize = len(server_guid)

        game_info.gameMode = ffi.new("char[]", game_mode.encode('utf-8'))
        game_info.gameModeSize = len(game_mode)

        game_guid = ffi.new("char[256]") 
        getgudsdk.StartGame(game_info[0], game_guid)

        return ffi.string(game_guid).decode('utf-8')

    def start_match(self, game_guid, match_mode, map_name):
        match_info = ffi.new("struct StartMatchInfo*")

        match_info.gameGuid = ffi.new("char[]", game_guid.encode('utf-8'))
        match_info.gameGuidSize = len(game_guid)

        match_info.matchMode = ffi.new("char[]", match_mode.encode('utf-8'))
        match_info.matchModeSize = len(match_mode)

        match_info.mapName = ffi.new("char[]", map_name.encode('utf-8'))
        match_info.mapNameSize = len(map_name)

        match_guid = ffi.new("char[256]")
        result_code = getgudsdk.StartMatch(match_info[0], match_guid)

        return ffi.string(match_guid).decode('utf-8')

    def mark_end_game(self, game_guid):
        return getgudsdk.MarkEndGame(game_guid.encode('utf-8'), len(game_guid))

    def send_in_match_report(self, match_guid, reporter_name, reporter_type, reporter_sub_type, 
                         suspected_player_guid, tb_type, tb_sub_type, 
                         tb_time_epoch, suggested_toxicity_score, reported_time_epoch):
        report_info = ffi.new("struct ReportInfo*")
        
        report_info.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        report_info.matchGuidSize = len(match_guid)

        report_info.reporterName = ffi.new("char[]", reporter_name.encode('utf-8'))
        report_info.reporterNameSize = len(reporter_name)

        report_info.reporterType = reporter_type
        report_info.reporterSubType = reporter_sub_type
        
        report_info.suspectedPlayerGuid = ffi.new("char[]", suspected_player_guid.encode('utf-8'))
        report_info.suspectedPlayerGuidSize = len(suspected_player_guid)

        report_info.tbType = tb_type
        report_info.tbSubType = tb_sub_type
        report_info.tbTimeEpoch = tb_time_epoch

        report_info.suggestedToxicityScore = suggested_toxicity_score
        report_info.reportedTimeEpoch = reported_time_epoch
        
        result_code = getgudsdk.SendInMatchReport(report_info[0])

        return result_code

    def send_chat_message(self, match_guid, message_time_epoch, player_guid, message):
        message_info = ffi.new("struct ChatMessageInfo*")

        message_info.messageTimeEpoch = message_time_epoch

        message_info.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        message_info.matchGuidSize = len(match_guid)

        message_info.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        message_info.playerGuidSize = len(player_guid)

        message_info.message = ffi.new("char[]", message.encode('utf-8'))
        message_info.messageSize = len(message)

        result_code = getgudsdk.SendChatMessage(message_info[0])

        return result_code
    
    def send_attack_action(self, match_guid, action_time_epoch, player_guid, weapon_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)
        
        weapon_guid_data = ffi.new("char[]", weapon_guid.encode('utf-8'))
        weapon_guid_size = len(weapon_guid)

        return getgudsdk.SendAttackAction(base_data[0], weapon_guid_data, weapon_guid_size)

    def send_damage_action(self, match_guid, action_time_epoch, player_guid,
                        victim_player_guid, damage_done, weapon_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)
        
        victim_player_guid_data = ffi.new("char[]", victim_player_guid.encode('utf-8'))
        victim_player_guid_size = len(victim_player_guid)
        weapon_guid_data = ffi.new("char[]", weapon_guid.encode('utf-8'))
        weapon_guid_size = len(weapon_guid)

        return getgudsdk.SendDamageAction(base_data[0], victim_player_guid_data,
                                        victim_player_guid_size, damage_done,
                                        weapon_guid_data, weapon_guid_size)

    def send_heal_action(self, match_guid, action_time_epoch, player_guid, health_gained):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)

        return getgudsdk.SendHealAction(base_data[0], health_gained)

    def send_spawn_action(self, match_guid, action_time_epoch, player_guid,
                        character_guid, team_id, initial_health, position, rotation):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)

        character_guid_data = ffi.new("char[]", character_guid.encode('utf-8'))
        character_guid_size = len(character_guid)

        position_struct = ffi.new("struct PositionF*", {"X": position[0], "Y": position[1], "Z": position[2]})
        rotation_struct = ffi.new("struct RotationF*", {"Pitch": rotation[0], "Roll": rotation[1]})

        return getgudsdk.SendSpawnAction(base_data[0], character_guid_data, character_guid_size,
                                        team_id, initial_health, position_struct[0], rotation_struct[0])

    def send_death_action(self, match_guid, action_time_epoch, player_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)

        return getgudsdk.SendDeathAction(base_data[0])

    def send_position_action(self, match_guid, action_time_epoch, player_guid, position, rotation):
        base_data = ffi.new("struct BaseActionData*")
        base_data.matchGuid = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuidSize = len(match_guid)
        base_data.actionTimeEpoch = action_time_epoch
        base_data.playerGuid = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuidSize = len(player_guid)

        position_struct = ffi.new("struct PositionF*", {"X": position[0], "Y": position[1], "Z": position[2]})
        rotation_struct = ffi.new("struct RotationF*", {"Pitch": rotation[0], "Roll": rotation[1]})

        return getgudsdk.SendPositionAction(base_data[0], position_struct[0], rotation_struct[0])
    
    def dispose(self):
        getgudsdk.dispose()
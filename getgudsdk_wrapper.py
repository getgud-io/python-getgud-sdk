import getgudsdk.lib as getgudsdk
from getgudsdk import ffi
import time

class GetGudSdk:
    def __init__(self):
        getgudsdk.init()

    def start_game(self, title_id, private_key, server_guid, game_mode):
        game_info = ffi.new("struct StartGameInfo*")
        game_info.titleId = title_id

        private_key_data = ffi.new("char[]", private_key.encode('utf-8'))
        game_info.privateKey = private_key_data
        game_info.privateKeySize = len(private_key)
        
        server_guid_data = ffi.new("char[]", server_guid.encode('utf-8'))
        game_info.serverGuid = server_guid_data
        game_info.serverGuidSize = len(server_guid)

        game_mode_data = ffi.new("char[]", game_mode.encode('utf-8'))
        game_info.gameMode = game_mode_data
        game_info.gameModeSize = len(game_mode)

        game_guid = ffi.new("char[256]") 
        getgudsdk.StartGame(game_info[0], game_guid)

        return ffi.string(game_guid).decode('utf-8')

    def start_match(self, game_guid, match_mode, map_name):
        match_info = ffi.new("struct StartMatchInfo*")

        game_guid_data = ffi.new("char[]", game_guid.encode('utf-8'))
        match_info.gameGuid = game_guid_data
        match_info.gameGuidSize = len(game_guid)

        match_mode_data = ffi.new("char[]", match_mode.encode('utf-8'))
        match_info.matchMode = match_mode_data
        match_info.matchModeSize = len(match_mode)

        map_name_data = ffi.new("char[]", map_name.encode('utf-8'))
        match_info.mapName = map_name_data
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
        
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        report_info.matchGuid = match_guid_data
        report_info.matchGuidSize = len(match_guid)

        reporter_name_data = ffi.new("char[]", reporter_name.encode('utf-8'))
        report_info.reporterName = reporter_name_data
        report_info.reporterNameSize = len(reporter_name)

        report_info.reporterType = reporter_type
        report_info.reporterSubType = reporter_sub_type
        
        suspected_player_data = ffi.new("char[]", suspected_player_guid.encode('utf-8'))
        report_info.suspectedPlayerGuid = suspected_player_data
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

        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        message_info.matchGuid = match_guid_data
        message_info.matchGuidSize = len(match_guid)

        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        message_info.playerGuid = player_guid_data
        message_info.playerGuidSize = len(player_guid)

        message_info_data = ffi.new("char[]", message.encode('utf-8'))
        message_info.message = message_info_data
        message_info.messageSize = len(message)

        result_code = getgudsdk.SendChatMessage(message_info[0])

        return result_code
    
    def send_attack_action(self, match_guid, action_time_epoch, player_guid, weapon_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
        base_data.playerGuidSize = len(player_guid)
        
        weapon_guid_data = ffi.new("char[]", weapon_guid.encode('utf-8'))
        weapon_guid_size = len(weapon_guid)

        return getgudsdk.SendAttackAction(base_data[0], weapon_guid_data, weapon_guid_size)

    def send_damage_action(self, match_guid, action_time_epoch, player_guid,
                        victim_player_guid, damage_done, weapon_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
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
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
        base_data.playerGuidSize = len(player_guid)

        return getgudsdk.SendHealAction(base_data[0], health_gained)

    def send_spawn_action(self, match_guid, action_time_epoch, player_guid,
                        character_guid, team_id, initial_health, position, rotation):
        base_data = ffi.new("struct BaseActionData*")
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
        base_data.playerGuidSize = len(player_guid)

        character_guid_data = ffi.new("char[]", character_guid.encode('utf-8'))
        character_guid_size = len(character_guid)

        position_struct = ffi.new("struct PositionF*", {"X": position[0], "Y": position[1], "Z": position[2]})
        rotation_struct = ffi.new("struct RotationF*", {"Yaw": rotation[0], "Pitch": rotation[1], "Roll": rotation[2]})

        return getgudsdk.SendSpawnAction(base_data[0], character_guid_data, character_guid_size,
                                        team_id, initial_health, position_struct[0], rotation_struct[0])


    
    def send_death_action(self, match_guid, action_time_epoch, player_guid):
        base_data = ffi.new("struct BaseActionData*")
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
        base_data.playerGuidSize = len(player_guid)

        return getgudsdk.SendDeathAction(base_data[0])

    def send_position_action(self, match_guid, action_time_epoch, player_guid, position, rotation):
        base_data = ffi.new("struct BaseActionData*")
        base_data.actionTimeEpoch = action_time_epoch
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        base_data.matchGuid = match_guid_data
        base_data.matchGuidSize = len(match_guid)
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        base_data.playerGuid = player_guid_data
        base_data.playerGuidSize = len(player_guid)

        position_struct = ffi.new("struct PositionF*", {"X": position[0], "Y": position[1], "Z": position[2]})
        rotation_struct = ffi.new("struct RotationF*", {"Yaw": rotation[0], "Pitch": rotation[1], "Roll": rotation[2]})

        return getgudsdk.SendPositionAction(base_data[0], position_struct[0], rotation_struct[0])
    
    def send_report(self, title_id, private_key, match_guid, reporter_name, reporter_type, reporter_sub_type, 
                         suspected_player_guid, tb_type, 
                         tb_time_epoch, suggested_toxicity_score, reported_time_epoch):
        
        private_key_data = ffi.new("char[]", private_key.encode('utf-8'))
        privateKeySize = len(private_key)
        
        report_info = ffi.new("struct ReportInfo*")
        
        match_guid_data = ffi.new("char[]", match_guid.encode('utf-8'))
        report_info.matchGuid = match_guid_data
        report_info.matchGuidSize = len(match_guid)

        reporter_name_data = ffi.new("char[]", reporter_name.encode('utf-8'))
        report_info.reporterName = reporter_name_data
        report_info.reporterNameSize = len(reporter_name)

        report_info.reporterType = reporter_type
        report_info.reporterSubType = reporter_sub_type
        
        suspected_player_data = ffi.new("char[]", suspected_player_guid.encode('utf-8'))
        report_info.suspectedPlayerGuid = suspected_player_data
        report_info.suspectedPlayerGuidSize = len(suspected_player_guid)

        report_info.tbType = tb_type
        report_info.tbTimeEpoch = tb_time_epoch

        report_info.suggestedToxicityScore = suggested_toxicity_score
        report_info.reportedTimeEpoch = reported_time_epoch
        
        result_code = getgudsdk.SendReport(title_id, private_key_data, privateKeySize, report_info[0])

        return result_code
    
    def update_player(self, title_id, private_key, player_guid, player_nickname, player_email,
                        player_rank, player_join_date_epoch):
        
        private_key_data = ffi.new("char[]", private_key.encode('utf-8'))
        privateKeySize = len(private_key)
        
        player_info = ffi.new("struct PlayerInfo*")
        
        player_guid_data = ffi.new("char[]", player_guid.encode('utf-8'))
        player_info.playerGuid = player_guid_data
        player_info.playerGuidSize = len(player_guid)

        player_nickname_data = ffi.new("char[]", player_nickname.encode('utf-8'))
        player_info.playerNickname = player_nickname_data
        player_info.reporterNameSize = len(player_nickname)

        player_email_data = ffi.new("char[]", player_email.encode('utf-8'))
        player_info.playerEmail = player_email_data
        player_info.playerEmailSize = len(player_email)

        player_info.playerRank = player_rank
        player_info.playerJoinDateEpoch = player_join_date_epoch
        
        result_code = getgudsdk.UpdatePlayer(title_id, private_key_data, privateKeySize, player_info[0])

        return result_code
    
    def dispose(self):
        getgudsdk.dispose()
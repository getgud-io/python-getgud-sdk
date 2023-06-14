enum Actions { None, Attack, Damage, Death, Heal, Position, Spawn };

struct PositionF {
  float X;
  float Y;
  float Z;
};

struct RotationF {
  float Yaw;
  float Pitch;
  float Roll;
};
struct BaseActionData {
  long long actionTimeEpoch;
  char* matchGuid;
  int matchGuidSize;
  char* playerGuid;
  int playerGuidSize;
};
struct StartGameInfo {
  int titleId;
  char* privateKey;
  int privateKeySize;
  char* serverGuid;
  int serverGuidSize;
  char* gameMode;
  int gameModeSize;
};

struct StartMatchInfo {
  char* gameGuid;
  int gameGuidSize;
  char* matchMode;
  int matchModeSize;
  char* mapName;
  int mapNameSize;
};

struct ChatMessageInfo {
  long long messageTimeEpoch;
  char* matchGuid;
  int matchGuidSize;
  char* playerGuid;
  int playerGuidSize;
  char* message;
  int messageSize;
};

struct PlayerInfo {
  char* playerGuid;
  int playerGuidSize;
  char* playerNickname;
  int playerNicknameSize;
  char* playerEmail;
  int playerEmailSize;
  int playerRank;
  long long playerJoinDateEpoch;
};

struct ReportInfo {
  char* matchGuid;
  int matchGuidSize;
  char* reporterName;
  int reporterNameSize;
  int reporterType;
  int reporterSubType;
  char* suspectedPlayerGuid;
  int suspectedPlayerGuidSize;
  int tbType;
  int tbSubType;
  long long tbTimeEpoch;
  int suggestedToxicityScore;
  long long reportedTimeEpoch;
};


int init();
int StartGame(struct StartGameInfo gameInfo, char* gameGuidOut);
int StartMatch(struct StartMatchInfo matchInfo, char* matchGuidOut);
int MarkEndGame(char* gameGuid, int guidSize);
int SendInMatchReport(struct ReportInfo reportInfo);
int SendChatMessage(struct ChatMessageInfo messageInfo);
int SendAttackAction(struct BaseActionData baseData,
                     char* weaponGuid,
                     int weaponGuidSize);
int SendDamageAction(struct BaseActionData baseData,
                     char* victimPlayerGuid,
                     int victimPlayerGuidSize,
                     float damageDone,
                     char* weaponGuid,
                     int weaponGuidSize);
int SendHealAction(struct BaseActionData baseData, float healthGained);
int SendSpawnAction(struct BaseActionData baseData,
                    char* characterGuid,
                    int characterGuidSize,
                    int teamId,
                    float initialHealth,
                    struct PositionF position,
                    struct RotationF rotation);
int SendDeathAction(struct BaseActionData baseData);
int SendPositionAction(struct BaseActionData baseData,
                       struct PositionF position,
                       struct RotationF rotation);
void dispose();
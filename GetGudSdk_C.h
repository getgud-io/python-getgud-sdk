enum Actions { None = -1, Affect, Attack, Damage, Death, Heal, Position, Spawn };
typedef enum { Attach, Activate, Deactivate, Detach } AffectState;

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
  long long tbTimeEpoch;
  int suggestedToxicityScore;
  long long reportedTimeEpoch;
};

/**
* Init:
*
* Init Getgud SDK
**/
int init();

/**
 * StartGame:
 *
 * Start new game
 * Returns size
 **/
int StartGame(struct StartGameInfo gameInfo, char* gameGuidOut);

/**
 * Start match:
 *
 * Start a new match for an existing game
 **/
int StartMatch(struct StartMatchInfo matchInfo, char* matchGuidOut);

/**
 * MarkEndGame:
 *
 * Mark started game as finished
 **/
int MarkEndGame(char* gameGuid, int guidSize);

/**
 * SendAffectAction:
 *
 **/
int SendAffectAction(struct BaseActionData baseData,
  char* affectGuid,
  int affectGuidSize,
  AffectState affectState);

/**
 * SendAttackAction:
 *
 **/
int SendAttackAction(struct BaseActionData baseData,
                     char* weaponGuid,
                     int weaponGuidSize);

/**
 * SendDamageAction:
 *
 **/
int SendDamageAction(struct BaseActionData baseData,
                     char* victimPlayerGuid,
                     int victimPlayerGuidSize,
                     float damageDone,
                     char* weaponGuid,
                     int weaponGuidSize);

/**
 * SendHealAction:
 *
 **/
int SendHealAction(struct BaseActionData baseData, float healthGained);

/**
 * SendSpawnAction:
 *
 **/
int SendSpawnAction(struct BaseActionData baseData,
                    char* characterGuid,
                    int characterGuidSize,
                    int teamId,
                    float initialHealth,
                    struct PositionF position,
                    struct RotationF rotation);

/**
 * SendDeathAction:
 *
 **/
int SendDeathAction(struct BaseActionData baseData);

/**
 * SendPositionAction:
 *
 **/
int SendPositionAction(struct BaseActionData baseData,
                       struct PositionF position,
                       struct RotationF rotation);
/**
 * SendInMatchReport:
 *
 * Send a report which belongs to specifc match which is now live
 **/
int SendInMatchReport(struct ReportInfo reportInfo);

/**
 * SendChatMessage:
 *
 *  Send a message which belongs to specifc match which is now live
 **/
int SendChatMessage(struct ChatMessageInfo messageInfo);

/**
 * SendReport:
 *
 * Send report which are outside of the live match
 **/
int SendReport(int titleId,
  char* privateKey, int privateKeySize, struct ReportInfo report);

/**
 * UpdatePlayer:
 *
 * Update player info outside of the live match
 **/
int UpdatePlayer(int titleId,
  char* privateKey, int privateKeySize, struct PlayerInfo player);

/**
 * Dispose:
 *
 **/
void dispose();


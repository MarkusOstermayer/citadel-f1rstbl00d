# HTL-FirstbloodFastApi

> [!NOTE]
> This is the firstblood application for the CTF-Citadel hosting platform.  
> Authentication token and other aspects such as discord token and channel are mentioned below

### Configuration
Some aspects of the bot can be configured via a configuration file.
As of now, this includes:
* The help-message that users get shown
* A embed that is getting send once a team gets a firstblood

### env vars:
The following environment variables are needed to make the stack function completly:
- BLOODTOKEN= {your_auth_token}
- DISCORD_TOKEN={"your_discord_bot_token"}
- DISCORD_CHANNEL_ID={"your_discord_channel_id"}

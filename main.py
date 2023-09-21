import os
from colorama import Fore, init
from pystyle import Colors, Colorate
import aiohttp
import asyncio

os.system(f"Title Nexus")
token = None
init(autoreset=True)

def banner():
    bann = """
       ███▄    █ ▓█████ ▒██   ██▒ █    ██   ██████       
       ██ ▀█   █ ▓█   ▀ ▒▒ █ █ ▒░ ██  ▓██▒▒██    ▒       
      ▓██  ▀█ ██▒▒███   ░░  █   ░▓██  ▒██░░ ▓██▄         
      ▓██▒  ▐▌██▒▒▓█  ▄  ░ █ █ ▒ ▓▓█  ░██░  ▒   ██▒      
      ▒██░   ▓██░░▒████▒▒██▒ ▒██▒▒▒█████▓ ▒██████▒▒      
      ░ ▒░   ▒ ▒ ░░ ▒░ ░▒▒ ░ ░▓ ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░      
      ░ ░░   ░ ▒░ ░ ░  ░░░   ░▒ ░░░▒░ ░ ░ ░ ░▒  ░ ░      
         ░   ░ ░    ░    ░    ░   ░░░ ░ ░ ░  ░  ░        
               ░    ░  ░ ░    ░     ░           ░        
                                                         \n"""
    print(Colorate.Diagonal(Colors.blue_to_green, bann, 2))

def options():
    opt = """┌────────────────────┬──────────────────────┬────────────────────┐
│ Discord: __crypt__ │  Discord: __crypt__  │ Discord: __crypt__ │
├────────────────────┼──────────────────────┼────────────────────┤
│ [1] Token checker  │ [6] Mass Roles       │ [11] Set Token     │
│ [2] Messager       │ [7] Channel Remover  │ [12] Set Webhook   │
│ [3] Channel Spam   │ [8] Channel Creator  │ [13] Get channels  │
│ [4] Mass Ban       │ [9] Webhook Remover  │ [14] Get invite    │
│ [5] Give Admin     │ [10] Webhook Spammer │ [15] Create invite │
└────────────────────┴──────────────────────┴────────────────────┘
│                                                                │
└────────────────────────────────────────────────────────────────┘
\n"""
    return Colorate.Vertical(Colors.blue_to_green, opt, 2)

async def token_checker(token):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = "https://discord.com/api/v10/users/@me/guilds"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print("Token is valid. User data:")
                print(data)
            else:
                print("Token not found or invalid. Please check your token.")

async def send_message(token, channel_id, message):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    payload = {"content": message}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                return "Message sent successfully."
            else:
                return f"Error sending message. Status code: {response.status}"

async def get_guild_channels(token, guild_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return f"Error fetching guild channels. Status code: {response.status}"

async def get_guild_invite(token, guild_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/invites"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return f"Error fetching server invite. Status code: {response.status}"

async def channel_spam(token, channel_id, message, num_messages, delay):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    payload = {
        "content": message
    }
    
    async with aiohttp.ClientSession() as session:
        for _ in range(num_messages):
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    print(f"Message {_+1}/{num_messages} sent successfully.")
                else:
                    print(f"Error sending message {_+1}/{num_messages}. Status code: {response.status}")
                await asyncio.sleep(delay)

async def get_guild_members(token, guild_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/members"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return f"Error fetching guild members. Status code: {response.status}"

async def ban_member(token, guild_id, user_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status == 204:
                return "Member banned successfully."
            else:
                return f"Error banning member. Status code: {response.status}"

async def create_admin_role(token, guild_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles"

    payload = {
        "name": "cool Guy",
        "permissions": 2147483647, 
        "color": 0xFF0000  
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 201:
                data = await response.json()
                role_id = data.get("id")
                return role_id
            else:
                return None

async def assign_role_to_user(token, guild_id, user_id, role_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status == 204:
                return "Role assigned to user successfully."
            else:
                return f"Error assigning role to user. Status code: {response.status}"

async def create_mass_roles(token, guild_id, num_roles, role_name):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles"
    
    async with aiohttp.ClientSession() as session:
        for i in range(num_roles):
            payload = {
                "name": role_name,
                "permissions": 0, 
                "color": 0xFFFFFF  
            }
            
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 201:
                    print(f"Failed to create role {i + 1}. Status code: {response.status}")

    print(f"{num_roles} roles created with the name '{role_name}' in the guild with ID {guild_id}.")

async def delete_channel(token, channel_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                print(f"Channel with ID {channel_id} has been deleted.")
            else:
                print(f"Error deleting channel with ID {channel_id}. Status code: {response.status}")

async def delete_all_channels(token, guild_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                channels = await response.json()
                for channel in channels:
                    channel_id = channel.get("id")
                    await delete_channel(token, channel_id)
                print(f"All channels in the guild with ID {guild_id} have been deleted.")
            else:
                print(f"Error fetching channels. Status code: {response.status}")

async def create_mass_channels(token, guild_id, num_channels, channel_name, channel_type):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    async with aiohttp.ClientSession() as session:
        for i in range(num_channels):
            payload = {
                "name": channel_name,
                "type": channel_type  
            }
            
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 201:
                    print(f"Failed to create channel {i + 1}. Status code: {response.status}")
    
    channel_type_str = "text" if channel_type == 0 else "voice"
    print(f"{num_channels} {channel_type_str} channels created with the name '{channel_name}' in the guild with ID {guild_id}.")

async def main():
    global token
    tool_name = "Home"
    show_table = True
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        if show_table:
            print(options())
        choice = input(f"nexus/{tool_name}> ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        elif show_table and choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 14:
                if choice == 1:
                    tool_name = "Token Checker"
                    inp = input("Enter the bot token: ")
                    await token_checker(inp)
                    input("Press enter to continue...")
                    tool_name = "Home"
                elif choice == 2:
                    tool_name = "Messager"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    channel_id = input("Enter the channel ID where you want to send the message: ")
                    message = input("Enter the message to be sent: ")
                    response = await send_message(inp, channel_id, message)
                    print(response)
                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 3:
                    tool_name = "Channel Spam"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    channel_id = input("Enter the channel ID where you want to send messages: ")
                    message = input("Enter the message to be sent: ")
                    num_messages = int(input("Enter the number of messages to send: "))
                    delay = float(input("Enter the delay (in seconds) between messages: "))

                    for _ in range(num_messages):
                        response = await send_message(inp, channel_id, message)
                        print(response)
                        await asyncio.sleep(delay)

                    print(f"Successfully sent {num_messages} messages with a {delay} second delay each.")
                    input("Press Enter to continue...")
                    tool_name = "Home"

                elif choice == 4:
                    tool_name = "Mass Ban"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID where you want to mass ban members: ")

                    members = await get_guild_members(inp, guild_id)
                    if isinstance(members, list):
                        for member in members:
                            user_id = member['user']['id']
                            await ban_member(inp, guild_id, user_id)
                        print(f"Successfully banned {len(members)} members in the guild with ID {guild_id}.")
                    else:
                        print(members)

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 5:
                    tool_name = "Give Admin"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID: ")
                    user_id = input("Enter the user ID: ")


                    role_id = await create_admin_role(inp, guild_id)

                    if role_id:

                        await assign_role_to_user(inp, guild_id, user_id, role_id)
                        print(f"Admin role created and assigned to user with ID {user_id} in the guild with ID {guild_id}.")
                    else:
                        print("Failed to create the admin role.")

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 6:
                    tool_name = "Mass Roles"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID where you want to create roles: ")
                    num_roles = int(input("Enter the number of roles to create: "))
                    role_name = input("Enter the role name: ")

                    await create_mass_roles(inp, guild_id, num_roles, role_name)

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 7:
                    tool_name = "Channel Remover"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID where you want to delete all channels: ")

                    await delete_all_channels(inp, guild_id)

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 8:
                    tool_name = "Channel Creator"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID where you want to create channels: ")
                    num_channels = int(input("Enter the number of channels to create: "))
                    channel_name = input("Enter the channel name: ")
                    channel_type = int(input("Enter the channel type (0 for text, 2 for voice): "))

                    await create_mass_channels(inp, guild_id, num_channels, channel_name, channel_type)

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 9:
                    tool_name = "Webhook Remover"
                elif choice == 10:
                    tool_name = "Webhook Spammer"
                elif choice == 11:
                    token = input("Enter your Discord bot token: ")
                    print(f"Token set to: {token}")
                    tool_name = "Set Token"
                    input("Press enter to continue...")
                    tool_name = "Home"
                elif choice == 12:
                    tool_name = "Set Webhook"
                elif choice == 13:
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID to check channels: ")
                    guild_channels = await get_guild_channels(inp, guild_id)
                    if isinstance(guild_channels, list):
                        print("Guild channels:")
                        for channel in guild_channels:
                            print(f"- {channel['name']} (ID: {channel['id']})")
                    else:
                        print(guild_channels)
                    tool_name = "Get Channels"
                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 14:
                    tool_name = "Get Invites"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            print("No existing token found. Please enter a new token.")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID to get the invite link: ")
                    invite_info = await get_guild_invite(inp, guild_id)
                    if isinstance(invite_info, dict):
                        print("Server Invite Link:")
                        print(invite_info.get("url"))
                    else:
                        print(invite_info)
                    input("Press Enter to continue...")
                    tool_name = "Home"
            else:
                print(Fore.RED + "Invalid option. Please select a valid option (1-12)." + Fore.RESET)
        elif not show_table and choice == "back":
            show_table = True
            tool_name = "home"
        else:
            print(Fore.RED + "Invalid input. Please enter a valid option or 'Q' to quit or 'back' to return to the home screen." + Fore.RESET)

        if show_table:
            print("Type 'back' to go to home")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

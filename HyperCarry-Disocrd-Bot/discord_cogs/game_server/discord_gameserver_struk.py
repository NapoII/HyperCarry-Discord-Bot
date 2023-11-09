# Searches all existing categories on the server for the category with the name "Rust".
category_name = "-----🖥️ - Server - 🖥️------"
category_server = discord.utils.get(guild.categories, name=category_name)

if category_server is not None:

    print(f"The category {category_server.name} already exists.")

else:
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view the category
        guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
    }


    print(f"The category {category_name} does not yet exist and will now be created")
    # Creates a new category
    category_server = await guild.create_category(category_name, overwrites=overwrites)
    print(f"The category {category_name} was created.")
    category_server_name = category_server.name
    category_server_id = category_server.id
    write_config(config_dir, "channel","category_server_id", category_server_id)

    Server_Stats = await guild.create_text_channel("📈 Server Stats", category=category_server)
    print(f"The channel {Server_Stats.name} was created.")

    server_stats_channel_id_name = Server_Stats.name
    server_stats_channel_id = Server_Stats.id
    write_config(config_dir, "Channel",
                    "server_stats_channel_id", server_stats_channel_id)
    #write_config(config_dir, "Channel", "server_stats_channel_id_name", server_stats_channel_id_name)

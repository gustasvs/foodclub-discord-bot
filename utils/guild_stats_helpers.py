def community_report(guild):
    online = 0
    afk = 0
    offline = 0
    for mem in guild.members:
        if str(mem.status) == "online":
            online += 1
        if str(mem.status) == "offline":
            offline += 1
        else:
            afk += 1
    return online, afk, offline
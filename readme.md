# Integrated D&D Game Manager

## Goal:
Provide basic web-based player and campaign management for Dungeons and Dragons 5e games. All users should be able to participate with a smartphone, tablet, or PC; either in person or remotely (with dialogue via Zoom, Skype, chat app support). Fill a gap between apps that handle one part of the game (character or campaign creation) but are not integrated ('Fight Club', 'Game Master'), and apps that are graphics-heavy and cumbersome ('D&D Beyond') 

## Target:
Current pen-and-paper players. Demographics, according to the publisher of the guidebooks (Wizards of the Coast), are 40/60% female/male, 75% between ages 20 and 39.

## Data:
( https://www.dnd5eapi.co/docs/ ) This data is available as part of the 'System Reference Document 5.1 (“SRD5”)' granted through use of the Open Gaming License, Version 1.0a.

This includes the basic rule set for D&D 5e games (player races, classes, monsters, combat mechanics, etc.). It should be sufficient for full character creation and equipping, tracking stats (XP, level, etc.), and building campaigns.

## Database Schema:
(many player-related tables with player_id PK/FK to break up player data)  

## Potential issues with API:
none foreseen

## Sensitive information to secure:
passwords for user accounts and for joining campaigns

## Functionality:
App should permit creation and editing of player characters (PCs) and campaigns. App should collect players into a single campaign, run by a single user (the 'dungeon master' or 'DM'). DMs should get access to player information without ability to edit. Players should get access to all of their own data, plus select data from other players in the campaign, as permitted by those players.
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 17:39:57 2022

@author: maurop
"""

import json


# =============================================================================
# Chat Member
# =============================================================================

class ChatMember:
    
    def __init__(self, chat_member_json):
        self.status = chat_member_json["status"]
        self.user = User(chat_member_json["user"])
        self.can_restrict_members = chat_member_json.get("can_restrict_members")
        
    def __str__(self):
        return f"Chat member: {self.user} {self.status}"

'''    
https://core.telegram.org/bots/api#chatmember
ChatMember
This object contains information about one member of a chat. Currently, the following 6 types of chat members are supported:

ChatMemberOwner
ChatMemberAdministrator
ChatMemberMember
ChatMemberRestricted
ChatMemberLeft
ChatMemberBanned

ChatMemberOwner
Represents a chat member that owns the chat and has all administrator privileges.

Field	Type	Description
status	String	The member's status in the chat, always “creator”
user	User	Information about the user
is_anonymous	Boolean	True, if the user's presence in the chat is hidden
custom_title	String	Optional. Custom title for this user

ChatMemberAdministrator
Represents a chat member that has some additional privileges.

Field	Type	Description
status	String	The member's status in the chat, always “administrator”
user	User	Information about the user
can_be_edited	Boolean	True, if the bot is allowed to edit administrator privileges of that user
is_anonymous	Boolean	True, if the user's presence in the chat is hidden
can_manage_chat	Boolean	True, if the administrator can access the chat event log, chat statistics, message statistics in channels, see channel members, see anonymous administrators in supergroups and ignore slow mode. Implied by any other administrator privilege
can_delete_messages	Boolean	True, if the administrator can delete messages of other users
can_manage_video_chats	Boolean	True, if the administrator can manage video chats
can_restrict_members	Boolean	True, if the administrator can restrict, ban or unban chat members
can_promote_members	Boolean	True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by the user)
can_change_info	Boolean	True, if the user is allowed to change the chat title, photo and other settings
can_invite_users	Boolean	True, if the user is allowed to invite new users to the chat
can_post_messages	Boolean	Optional. True, if the administrator can post in the channel; channels only
can_edit_messages	Boolean	Optional. True, if the administrator can edit messages of other users and can pin messages; channels only
can_pin_messages	Boolean	Optional. True, if the user is allowed to pin messages; groups and supergroups only
custom_title	String	Optional. Custom title for this user

ChatMemberMember
Represents a chat member that has no additional privileges or restrictions.

Field	Type	Description
status	String	The member's status in the chat, always “member”
user	User	Information about the user

ChatMemberRestricted
Represents a chat member that is under certain restrictions in the chat. Supergroups only.

Field	Type	Description
status	String	The member's status in the chat, always “restricted”
user	User	Information about the user
is_member	Boolean	True, if the user is a member of the chat at the moment of the request
can_change_info	Boolean	True, if the user is allowed to change the chat title, photo and other settings
can_invite_users	Boolean	True, if the user is allowed to invite new users to the chat
can_pin_messages	Boolean	True, if the user is allowed to pin messages
can_send_messages	Boolean	True, if the user is allowed to send text messages, contacts, locations and venues
can_send_media_messages	Boolean	True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes
can_send_polls	Boolean	True, if the user is allowed to send polls
can_send_other_messages	Boolean	True, if the user is allowed to send animations, games, stickers and use inline bots
can_add_web_page_previews	Boolean	True, if the user is allowed to add web page previews to their messages
until_date	Integer	Date when restrictions will be lifted for this user; unix time. If 0, then the user is restricted forever

ChatMemberLeft
Represents a chat member that isn't currently a member of the chat, but may join it themselves.

Field	Type	Description
status	String	The member's status in the chat, always “left”
user	User	Information about the user

ChatMemberBanned
Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.

Field	Type	Description
status	String	The member's status in the chat, always “kicked”
user	User	Information about the user
until_date	Integer	Date when restrictions will be lifted for this user; unix time. If 0, then the user is banned forever
'''
        
# =============================================================================
# User
# =============================================================================


class User:
    
    def __init__(self, user_json):
        self.id = user_json["id"]
        self.is_bot = user_json["is_bot"]
        self.first_name = user_json["first_name"]
        
        self.last_name = user_json.get("last_name")
        self.username = user_json.get("username")
        self.language_code = user_json.get("language_code")
        self.is_premium = user_json.get("is_premium")
        self.added_to_attachment_menu = user_json.get("added_to_attachment_menu")
        self.can_join_groups = user_json.get("can_join_groups")
        self.can_read_all_group_messages = user_json.get("can_read_all_group_messages")
        self.supports_inline_queries = user_json.get("supports_inline_queries")
    
    def has_changed(self, user):
        
        if self.first_name != user.first_name:
            return True
        
        if self.last_name != user.last_name:
            return True
        
        if self.username != user.username:
            return True
        
        return False
    
    def get_mention_link(self):
        s = "<a href=\"tg://user?id={}\">_{}_</a>".format(self.id, self.first_name)
        return s
        
        
    def get_silent(self):
        return f"{self.first_name}" +  f" (@ {self.username})" if self.username else ""

    
    def __str__(self):
        name = f"{self.first_name}"
        return name +  (f" (@{self.username})" if self.username else "")
        
        
        
        

        
'''
This object represents a Telegram user or bot.

Field	Type	Description
id	Integer	Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
is_bot	Boolean	True, if this user is a bot
first_name	String	User's or bot's first name
last_name	String	Optional. User's or bot's last name
username	String	Optional. User's or bot's username
language_code	String	Optional. IETF language tag of the user's language
is_premium	True	Optional. True, if this user is a Telegram Premium user
added_to_attachment_menu	True	Optional. True, if this user added the bot to the attachment menu
can_join_groups	Boolean	Optional. True, if the bot can be invited to groups. Returned only in getMe.
can_read_all_group_messages	Boolean	Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
supports_inline_queries	Boolean	Optional. True, if the bot supports inline queries. Returned only in getMe.
'''

# =============================================================================
# InlineKeyboard
# =============================================================================


class InlineKeyboardMarkup:
    
    def __init__(self):
        self.inline_keyboard = []
        
    def add_button(self, row, button):
        ''' add a button to the keyboard, with the corresponding row'''
        
        if len(self.inline_keyboard) <= row:
            for i in range(row - len(self.inline_keyboard)  + 1):
                self.inline_keyboard.append([])
                
        self.inline_keyboard[row].append(button.to_json())
    

    def to_json(self):
        return json.dumps({"inline_keyboard":self.inline_keyboard})
        
        


class InlineKeyboardButton:
    
    def __init__(self, text, url=None, callback_data=None, web_app=None, login_url=None, switch_inline_query=None):
        
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.web_app = web_app
        self.login_url = login_url
        self.switch_inline_query = switch_inline_query  
        
    
    def to_json(self):
        json_data = {}
        for key, value in self.__dict__.items():
            if value:
                json_data[key] = value
        
        return json_data
    
    
    
    
    
        

'''
InlineKeyboardMarkup
This object represents an inline keyboard that appears right next to the message it belongs to.

Field	Type	Description
inline_keyboard	Array of Array of InlineKeyboardButton	Array of button rows, each represented by an Array of InlineKeyboardButton objects
Note: This will only work in Telegram versions released after 9 April, 2016. Older clients will display unsupported message.

InlineKeyboardButton
This object represents one button of an inline keyboard. You must use exactly one of the optional fields.

Field	Type	Description
text	String	Label text on the button
url	String	Optional. HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id=<user_id> can be used to mention a user by their ID without using a username, if this is allowed by their privacy settings.
callback_data	String	Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
web_app	WebAppInfo	Optional. Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Available only in private chats between a user and the bot.
login_url	LoginUrl	Optional. An HTTPS URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.
switch_inline_query	String	Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. May be empty, in which case just the bot's username will be inserted.

Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private chat with it. Especially useful when combined with switch_pm… actions - in this case the user will be automatically returned to the chat they switched from, skipping the chat selection screen.
switch_inline_query_current_chat	String	Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. May be empty, in which case only the bot's username will be inserted.

This offers a quick way for the user to open your bot in inline mode in the same chat - good for selecting something from multiple options.
callback_game	CallbackGame	Optional. Description of the game that will be launched when the user presses the button.

NOTE: This type of button must always be the first button in the first row.
pay	Boolean	Optional. Specify True, to send a Pay button.

NOTE: This type of button must always be the first button in the first row and can only be used in invoice messages.
'''

# =============================================================================
# Callback query
# =============================================================================


class CallbackQuery:
    
    def __init__(self, query_json):
        
        self.id = query_json["id"]
        self.user = User(query_json["from"])
        
        message = query_json.get("message")
        self.message = Message(message) if message else None
        
        self.inline_message_id = query_json.get("inline_message_id")
        self.chat_instance = query_json["chat_instance"]
        self.data = query_json.get("data")
        self.game_short_name = query_json.get("game_short_name")
        
        
        
        

'''
CallbackQuery
This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.

Field	Type	Description
id	String	Unique identifier for this query
from	User	Sender
message	Message	Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
inline_message_id	String	Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
chat_instance	String	Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
data	String	Optional. Data associated with the callback button. Be aware that the message originated the query can contain no callback buttons with this data.
game_short_name	String	Optional. Short name of a Game to be returned, serves as the unique identifier for the game
NOTE: After the user presses a callback button, Telegram clients will display a progress bar until you call answerCallbackQuery. It is, therefore, necessary to react by calling answerCallbackQuery even if no notification to the user is needed (e.g., without specifying any of the optional parameters).
'''


# =============================================================================
# Chat                
# =============================================================================

class Chat:
    
    def __init__(self, chat_json):
        
        self.id = chat_json["id"]
        self.type = chat_json["type"]
        self.title = chat_json.get("title")
        self.username = chat_json.get("username")
        self.first_name = chat_json.get("first_name")
        self.last_name = chat_json.get("last_name")
        # self.photo (not implemented yet)
        
        self.bio = chat_json.get("bio")
        self.has_private_forwards = chat_json.get("has_private_forwards")
                
        self.has_restricted_voice_and_video_messages = chat_json.get("has_restricted_voice_and_video_messages")
        self.join_to_send_messages = chat_json.get("join_to_send_messages")
        self.join_by_request = chat_json.get("join_by_request")
        self.description = chat_json.get("description")
        self.invite_link = chat_json.get("invite_link")
        
        pinned_message = chat_json.get("pinned_message")
        self.pinned_message = Message(pinned_message) if pinned_message else None
        #self.permissions = chat_json.get("permissions")
        self.slow_mode_delay = chat_json.get("slow_mode_delay")
        self.message_auto_delete_time = chat_json.get("message_auto_delete_time")
        self.has_protected_content = chat_json.get("has_protected_content")
        self.sticker_set_name = chat_json.get("sticker_set_name")
        self.can_set_sticker_set = chat_json.get("can_set_sticker_set")
        self.linked_chat_id = chat_json.get("linked_chat_id")
        #self.location = chat_json.get("location")





'''
Chat
This object represents a chat.

Field	Type	Description
id	Integer	Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
type	String	Type of chat, can be either “private”, “group”, “supergroup” or “channel”
title	String	Optional. Title, for supergroups, channels and group chats
username	String	Optional. Username, for private chats, supergroups and channels if available
first_name	String	Optional. First name of the other party in a private chat
last_name	String	Optional. Last name of the other party in a private chat
photo	ChatPhoto	Optional. Chat photo. Returned only in getChat.
bio	String	Optional. Bio of the other party in a private chat. Returned only in getChat.
has_private_forwards	True	Optional. True, if privacy settings of the other party in the private chat allows to use tg://user?id=<user_id> links only in chats with the user. Returned only in getChat.
has_restricted_voice_and_video_messages	True	Optional. True, if the privacy settings of the other party restrict sending voice and video note messages in the private chat. Returned only in getChat.
join_to_send_messages	True	Optional. True, if users need to join the supergroup before they can send messages. Returned only in getChat.
join_by_request	True	Optional. True, if all users directly joining the supergroup need to be approved by supergroup administrators. Returned only in getChat.
description	String	Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.
invite_link	String	Optional. Primary invite link, for groups, supergroups and channel chats. Returned only in getChat.
pinned_message	Message	Optional. The most recent pinned message (by sending date). Returned only in getChat.
permissions	ChatPermissions	Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
slow_mode_delay	Integer	Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user; in seconds. Returned only in getChat.
message_auto_delete_time	Integer	Optional. The time after which all messages sent to the chat will be automatically deleted; in seconds. Returned only in getChat.
has_protected_content	True	Optional. True, if messages from the chat can't be forwarded to other chats. Returned only in getChat.
sticker_set_name	String	Optional. For supergroups, name of group sticker set. Returned only in getChat.
can_set_sticker_set	True	Optional. True, if the bot can change the group sticker set. Returned only in getChat.
linked_chat_id	Integer	Optional. Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; for supergroups and channel chats. This identifier may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier. Returned only in getChat.
location	ChatLocation	Optional. For supergroups, the location to which the supergroup is connected. Returned only in getChat.
'''                
# =============================================================================
# Message            
# =============================================================================

class Message:
    
    def __init__(self, message_json):
        self.message_id = message_json["message_id"]
        self.user = User(message_json["from"])
        
        sender_chat = message_json.get("sender_chat")
        self.sender_chat = Chat(sender_chat) if sender_chat else None
        
        self.date = message_json["date"]
        self.chat = Chat(message_json["chat"])
        
        forward_from = message_json.get("forward_from")
        self.forward_from = User(forward_from) if forward_from else None
        
        forward_from_chat = message_json.get("forward_from_chat")
        self.forward_from_chat = forward_from_chat if forward_from_chat else None
        
        # self.forward_from_message_id
        # self.forward_signature
        # self.forward_sender_name
        # self.forward_date
        # self.is_automatic_forward
        # self.reply_to_message
        # self.via_bot
        # self.edit_date
        # self.has_protected_content
        # self.media_group_id
        # self.author_signature
        
        text = message_json.get("text")
        self.text = text if text else None
        
        self.photos = []
        
        if message_json.get("photo"):
            self.photos = PhotoSizeArray(message_json["photo"])
        
        # self.entities
        # self.animation
        # self.audio
        
        document = message_json.get("document")
        self.document = Document(document) if document else None
        
        # self.photo
        # self.sticker
        # self.video
        # self.video_note
        # self.voice
        # self.caption
        # self.caption_entities
        # self.contact
        # self.dice
        # self.game
        # self.poll
        # self.venue
        # self.location
        # self.new_chat_members
        # self.left_chat_member
        # self.new_chat_title
        # self.new_chat_photo
        # self.delete_chat_photo
        # self.group_chat_created
        # self.supergroup_chat_created
        # self.channel_chat_created
        # self.message_auto_delete_timer_changed
        # self.migrate_to_chat_id
        # self.migrate_from_chat_id
        # self.pinned_message
        # self.invoice
        # self.successful_payment
        # self.connected_website
        # self.passport_data
        # self.proximity_alert_triggered
        # self.video_chat_scheduled
        # self.video_chat_started
        # self.video_chat_ended
        # self.video_chat_participants_invited
        # self.web_app_data
        # self.reply_markup
        
        self.json_data = message_json

        
        

        
'''
Message
This object represents a message.

Field	Type	Description
message_id	Integer	Unique message identifier inside this chat
from	User	Optional. Sender of the message; empty for messages sent to channels. For backward compatibility, the field contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
sender_chat	Chat	Optional. Sender of the message, sent on behalf of a chat. For example, the channel itself for channel posts, the supergroup itself for messages from anonymous group administrators, the linked channel for messages automatically forwarded to the discussion group. For backward compatibility, the field from contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
date	Integer	Date the message was sent in Unix time
chat	Chat	Conversation the message belongs to
forward_from	User	Optional. For forwarded messages, sender of the original message
forward_from_chat	Chat	Optional. For messages forwarded from channels or from anonymous administrators, information about the original sender chat
forward_from_message_id	Integer	Optional. For messages forwarded from channels, identifier of the original message in the channel
forward_signature	String	Optional. For forwarded messages that were originally sent in channels or by an anonymous chat administrator, signature of the message sender if present
forward_sender_name	String	Optional. Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
forward_date	Integer	Optional. For forwarded messages, date the original message was sent in Unix time
is_automatic_forward	True	Optional. True, if the message is a channel post that was automatically forwarded to the connected discussion group
reply_to_message	Message	Optional. For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
via_bot	User	Optional. Bot through which the message was sent
edit_date	Integer	Optional. Date the message was last edited in Unix time
has_protected_content	True	Optional. True, if the message can't be forwarded
media_group_id	String	Optional. The unique identifier of a media message group this message belongs to
author_signature	String	Optional. Signature of the post author for messages in channels, or the custom title of an anonymous group administrator
text	String	Optional. For text messages, the actual UTF-8 text of the message
entities	Array of MessageEntity	Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
animation	Animation	Optional. Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set
audio	Audio	Optional. Message is an audio file, information about the file
document	Document	Optional. Message is a general file, information about the file
photo	Array of PhotoSize	Optional. Message is a photo, available sizes of the photo
sticker	Sticker	Optional. Message is a sticker, information about the sticker
video	Video	Optional. Message is a video, information about the video
video_note	VideoNote	Optional. Message is a video note, information about the video message
voice	Voice	Optional. Message is a voice message, information about the file
caption	String	Optional. Caption for the animation, audio, document, photo, video or voice
caption_entities	Array of MessageEntity	Optional. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
contact	Contact	Optional. Message is a shared contact, information about the contact
dice	Dice	Optional. Message is a dice with random value
game	Game	Optional. Message is a game, information about the game. More about games »
poll	Poll	Optional. Message is a native poll, information about the poll
venue	Venue	Optional. Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set
location	Location	Optional. Message is a shared location, information about the location
new_chat_members	Array of User	Optional. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
left_chat_member	User	Optional. A member was removed from the group, information about them (this member may be the bot itself)
new_chat_title	String	Optional. A chat title was changed to this value
new_chat_photo	Array of PhotoSize	Optional. A chat photo was change to this value
delete_chat_photo	True	Optional. Service message: the chat photo was deleted
group_chat_created	True	Optional. Service message: the group has been created
supergroup_chat_created	True	Optional. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
channel_chat_created	True	Optional. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
message_auto_delete_timer_changed	MessageAutoDeleteTimerChanged	Optional. Service message: auto-delete timer settings changed in the chat
migrate_to_chat_id	Integer	Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
migrate_from_chat_id	Integer	Optional. The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
pinned_message	Message	Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itself a reply.
invoice	Invoice	Optional. Message is an invoice for a payment, information about the invoice. More about payments »
successful_payment	SuccessfulPayment	Optional. Message is a service message about a successful payment, information about the payment. More about payments »
connected_website	String	Optional. The domain name of the website on which the user has logged in. More about Telegram Login »
passport_data	PassportData	Optional. Telegram Passport data
proximity_alert_triggered	ProximityAlertTriggered	Optional. Service message. A user in the chat triggered another user's proximity alert while sharing Live Location.
video_chat_scheduled	VideoChatScheduled	Optional. Service message: video chat scheduled
video_chat_started	VideoChatStarted	Optional. Service message: video chat started
video_chat_ended	VideoChatEnded	Optional. Service message: video chat ended
video_chat_participants_invited	VideoChatParticipantsInvited	Optional. Service message: new participants invited to a video chat
web_app_data	WebAppData	Optional. Service message: data sent by a Web App
reply_markup	InlineKeyboardMarkup	Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
'''        


# =============================================================================
# Inline query        
# =============================================================================


# =============================================================================
# InlineQuery
# =============================================================================

class InlineQuery:

    def __init__(self, inline_query_json):
        self.id = inline_query_json["id"]
        self.user = User(inline_query_json["from"])
        self.text = inline_query_json["query"]
        self.offset = inline_query_json["offset"]

        self.chat_type = inline_query_json.get("chat_type")
        self.location = inline_query_json.get("location")


'''
InlineQuery
This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.

Field  Type    Description
id     String  Unique identifier for this query
from   User    Sender
query  String  Text of the query (up to 256 characters)
offset String  Offset of the results to be returned, can be controlled by the bot
chat_type      String  Optional. Type of the chat from which the inline query was sent. Can be either <E2><80><9C>sender<E2><80><9D> for a private chat with the inline query sender, <E2><80><9C>private<E2><80><9D>, <E2><80><9C>group<E2><80><9D>, <E2><80><9C>supergroup<E2><80><9D>, or <E2><80><9C>channel<E2><80><9D>. The chat type should be always known for requests sent from official clients and most third-party clients, unless the request was sent from a secret chat
location       Location        Optional. Sender location, only for bots that request user location
'''


# =============================================================================
# PhotoSize
# =============================================================================

class PhotoSize:
    
    def __init__(self, photo_size_json):
        self.file_id = photo_size_json["file_id"]
        self.file_unique_id = photo_size_json["file_unique_id"]
        self.width = photo_size_json["width"]
        self.height = photo_size_json["height"]
        self.file_size = photo_size_json.get("file_size")
       
'''PhotoSize
This object represents one size of a photo or a file / sticker thumbnail.

Field	Type	Description
file_id	String	Identifier for this file, which can be used to download or reuse the file
file_unique_id	String	Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
width	Integer	Photo width
height	Integer	Photo height
file_size	Integer	Optional. File size in bytes'''

class PhotoSizeArray:
    
    
    def __init__(self, array_photo_size_json):
        self.array = []
        for photo_json in array_photo_size_json:
            self.array.append(PhotoSize(photo_json))
            
            
    def get_highest_res(self):
        return max(self.array, key= lambda x : x.file_size)
    
    def get_lowsest_res(self):
        return min(self.array, key= lambda x : x.file_size)
    
# =============================================================================
# File
# =============================================================================

class File:
    
    def __init__(self, file_json):
        self.file_id = file_json["file_id"]
        self.file_unique_id = file_json["file_unique_id"]
        self.file_size = file_json.get("file_size")
        self.file_path = file_json.get("file_path")
        
        
        
'''File
This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile.

The maximum file size to download is 20 MB

Field	Type	Description
file_id	String	Identifier for this file, which can be used to download or reuse the file
file_unique_id	String	Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
file_size	Integer	Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value.
file_path	String	Optional. File path. Use https://api.telegram.org/file/bot<token>/<file_path> to get the file.'''


# =============================================================================
# Input Media
# =============================================================================

class InputMedia:
    
    def __init__(self, media_json):
        self.type = media_json["type"]
        self.media = media_json["media"]
        self.caption = media_json.get("caption")
        self.parse_mode = media_json.get("parse_mode")
        self.caption_entities = media_json.get("caption_entities")
    

'''
InputMedia
This object represents the content of a media message to be sent. It should be one of

InputMediaAnimation
InputMediaDocument
InputMediaAudio
InputMediaPhoto
InputMediaVideo

InputMediaPhoto
Represents a photo to be sent.

Field	Type	Description
type	String	Type of the result, must be photo
media	String	File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »
caption	String	Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
parse_mode	String	Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
caption_entities	Array of MessageEntity	Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode

InputMediaVideo
Represents a video to be sent.

Field	Type	Description
type	String	Type of the result, must be video
media	String	File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »
thumb	InputFile or String	Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »
caption	String	Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
parse_mode	String	Optional. Mode for parsing entities in the video caption. See formatting options for more details.
caption_entities	Array of MessageEntity	Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
width	Integer	Optional. Video width
height	Integer	Optional. Video height
duration	Integer	Optional. Video duration in seconds
supports_streaming	Boolean	Optional. Pass True if the uploaded video is suitable for streaming
InputMediaAnimation
Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.

Field	Type	Description
type	String	Type of the result, must be animation
media	String	File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »
thumb	InputFile or String	Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »
caption	String	Optional. Caption of the animation to be sent, 0-1024 characters after entities parsing
parse_mode	String	Optional. Mode for parsing entities in the animation caption. See formatting options for more details.
caption_entities	Array of MessageEntity	Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
width	Integer	Optional. Animation width
height	Integer	Optional. Animation height
duration	Integer	Optional. Animation duration in seconds
InputMediaAudio
Represents an audio file to be treated as music to be sent.

Field	Type	Description
type	String	Type of the result, must be audio
media	String	File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »
thumb	InputFile or String	Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »
caption	String	Optional. Caption of the audio to be sent, 0-1024 characters after entities parsing
parse_mode	String	Optional. Mode for parsing entities in the audio caption. See formatting options for more details.
caption_entities	Array of MessageEntity	Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
duration	Integer	Optional. Duration of the audio in seconds
performer	String	Optional. Performer of the audio
title	String	Optional. Title of the audio
InputMediaDocument
Represents a general file to be sent.

Field	Type	Description
type	String	Type of the result, must be document
media	String	File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »
thumb	InputFile or String	Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »
caption	String	Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
parse_mode	String	Optional. Mode for parsing entities in the document caption. See formatting options for more details.
caption_entities	Array of MessageEntity	Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
disable_content_type_detection	Boolean	Optional. Disables automatic server-side content type detection for files uploaded using multipart/form-data. Always True, if the document is sent as part of an album.
InputFile
This object represents the contents of a file to be uploaded. Must be posted using multipart/form-data in the usual way that files are uploaded via the browser.

Sending files
There are three ways to send files (photos, stickers, audio, media, etc.):

If the file is already stored somewhere on the Telegram servers, you don't need to reupload it: each file object has a file_id field, simply pass this file_id as a parameter instead of uploading. There are no limits for files sent this way.
Provide Telegram with an HTTP URL for the file to be sent. Telegram will download and send the file. 5 MB max size for photos and 20 MB max for other types of content.
Post the file using multipart/form-data in the usual way that files are uploaded via the browser. 10 MB max size for photos, 50 MB for other files.
Sending by file_id

It is not possible to change the file type when resending by file_id. I.e. a video can't be sent as a photo, a photo can't be sent as a document, etc.
It is not possible to resend thumbnails.
Resending a photo by file_id will send all of its sizes.
file_id is unique for each individual bot and can't be transferred from one bot to another.
file_id uniquely identifies a file, but a file can have different valid file_ids even for the same bot.
Sending by URL

When sending by URL the target file must have the correct MIME type (e.g., audio/mpeg for sendAudio, etc.).
In sendDocument, sending by URL will currently only work for GIF, PDF and ZIP files.
To use sendVoice, the file must have the type audio/ogg and be no more than 1MB in size. 1-20MB voice notes will be sent as files.
Other configurations may work but we can't guarantee that they will.
'''


# =============================================================================
# Document
# =============================================================================

class Document:
    
    def __init__(self, document_json):
        self.file_id = document_json["file_id"]
        self.file_unique_id = document_json["file_unique_id"]
        
        self.thumb = document_json.get("thumb")
        self.file_name = document_json.get("file_name")
        self.mime_type = document_json.get("mime_type")
        self.file_size = document_json.get("file_size")

'''
Document
This object represents a general file (as opposed to photos, voice messages and audio files).

Field	Type	Description
file_id	String	Identifier for this file, which can be used to download or reuse the file
file_unique_id	String	Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
thumb	PhotoSize	Optional. Document thumbnail as defined by sender
file_name	String	Optional. Original filename as defined by sender
mime_type	String	Optional. MIME type of the file as defined by sender
file_size	Integer	Optional. File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value.
'''
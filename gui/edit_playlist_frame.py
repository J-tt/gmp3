"""Edit a playlist frame."""

import wx, application
from gmusicapi.exceptions import NotLoggedIn
from wx.lib.sized_controls import SizedFrame
from wxgoodies.keys import add_accelerator
from db import session
from functions.util import do_login, do_error, delete_playlist

class EditPlaylistFrame(SizedFrame):
 """A frame for editing playlists."""
 def __init__(self, playlist):
  """Initialise with a playlist."""
  self.playlist = playlist
  super(EditPlaylistFrame, self).__init__(None, title = 'Playlist Editor')
  add_accelerator(self, 'ESCAPE', lambda event: self.Close(True))
  p = self.GetContentsPane()
  p.SetSizerType('form')
  wx.StaticText(p, label = '&Name')
  self.name = wx.TextCtrl(p, value = playlist.name, style = wx.TE_RICH2)
  wx.StaticText(p, label = '&Description')
  self.description = wx.TextCtrl(p, value = playlist.description, style = wx.TE_MULTILINE | wx.TE_RICH2)
  self.delete = wx.Button(p, label = 'D&elete')
  self.ok = wx.Button(p, label = '&OK')
  self.delete.Bind(wx.EVT_BUTTON, self.on_delete)
  self.ok.Bind(wx.EVT_BUTTON, self.on_ok)
 
 def on_delete(self, event):
  """Delete this playlist."""
  if wx.MessageBox('Are you sure you want to delete the %s playlist?' % self.playlist.name, 'Really Delete', style = wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
   if delete_playlist(self.playlist):
    self.Close(True)
   else:
    return do_error('Could not delete the %s playlist.' % self.playlist.name)
 
 def on_ok(self, event):
  """The OK button was pressed."""
  name, description = self.name.GetValue(), self.description.GetValue()
  if not name:
   return do_error('Playlist names cannot be blank.')
  elif not description:
   return do_error('Playlist descriptions cannot be blank.')
  else:
   self.playlist.name = name
   self.playlist.description = description
   try:
    self.playlist.id = application.api.edit_playlist(self.playlist.id, new_name = name, new_description = description)
   except NotLoggedIn:
    return do_login(callback = self.on_ok, args = [event])
   session.add(self.playlist)
   session.commit()
   self.Close(True)

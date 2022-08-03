# some constant definitions

kMargin_left        = 10
kMargin_top         = 3

# item duple offsets
kIndex_index        = 0
kIndex_id           = 1
kIndex_name         = 2
kIndex_flags        = 3

# Command IDs
# Connection management
kMenuID_connect     = 'connect'     # connect to FTP server by URL
kMenuID_connect_rand= 'connect_rand'# connect to random FTP server
kMenuID_disconnect  = 'disconnect'  # disconnect from FTP server
# Local directory operations
kMenuID_loc_label   = 'LOCAL'       # just a label
kMenuID_loc_list    = 'loc_list'    # list files in local working directory
kMenuID_loc_search  = 'loc_search'  # search for file in local working directory
kMenuID_loc_cwd     = 'loc_cwd'     # change local working directory
kMenuID_loc_ren     = 'loc_ren'     # rename local file or directory
kMenuID_loc_mkdir   = 'loc_mkdir'   # create local directory
kMenuID_loc_rm      = 'loc_rm'      # delete local file or directory
# Remote directory operations
kMenuID_rem_label   = 'REMOTE'      # just a label
kMenuID_rem_list    = 'rem_list'    # list files in remote working directory
kMenuID_rem_search  = 'rem_search'  # search for file in remote working directory
kMenuID_rem_cwd     = 'rem_cwd'     # change remote working directory
kMenuID_rem_ren     = 'rem_ren'     # rename remote file or directory
kMenuID_rem_mkdir   = 'rem_mkdir'   # create remote directory
kMenuID_rem_rm      = 'rem_rm'      # delete remote file or directory
# File transfer operations
kMenuID_upload      = 'upload'      # upload file(s)
kMenuID_download    = 'download'    # download file(s)
# Other
kMenuID_separator   = '---'         # NOP
kMenuID_quit        = 'quit'        # terminate this crazy app

kMenuFlag_disabled  = 'disabled'
kMenuFlag_separator = 'separator'

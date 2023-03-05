class ConfigInterface():
    
    USER_REPOS       = {"s_repo": "sessions", "t_repo": "templates"}
    SESSION_REPOS    = {"src": "src"}
    TEMPLATE_REPOS   = {"src": "src"}
    
    USER_DATA        = "user.json"
    SESSION_DATA     = "session.json"
    TEMPLATE_DATA    = "template.json"
    
    BASE_PATH        = "/var/vkr"
    GL_USERS_PATH    = BASE_PATH + "/users"
    GL_SESSION_PATH  = BASE_PATH + "/sessions"
    GL_TEMPLATE_PATH = BASE_PATH + "/templates"
    
    PRESETS_PATH     = "/app/src/app/presets"
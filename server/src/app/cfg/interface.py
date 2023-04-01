class ConfigInterface():
    
    USER_REPOS        = {"p_repo": "projects", "t_repo": "templates"}
    PROJECT_REPOS     = {"src": "src"}
    
    USER_DATA         = "user.json"
    PROJECT_DATA      = "project.json"
    
    BASE_PATH         = "/var/vkr"
    GL_USERS_PATH     = BASE_PATH + "/users"
    GL_PROJECT_PATH   = BASE_PATH + "/projects"
    GL_TEMPLATES_PATH = BASE_PATH + "/templates"
    GL_PUBLIC_PATH    = BASE_PATH + "/public"
    
    PRESETS_PATH      = "/app/src/app/templates"

    class Roles():
        ADMIN   = 1 
        TEACHER = 2
        STUDENT = 3

    ROLES = Roles()
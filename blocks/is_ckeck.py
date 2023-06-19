# check if the video is specifically categorized
def is_anal(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['anal']
            break
    return output


# check if the video is specifically categorized
def is_liked(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['likes']
            break
    return output


# check if the video is specifically categorized
def is_black(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['black']
            break
    return output


# check if the video is specifically categorized
def is_zmz(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['zmz']
            break
    return output


# check if the video is specifically categorized
def is_mzm(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['mzm']
            break
    return output


# check if the video is specifically categorized
def is_groop(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['groop']
            break
    return output


# check if the video is specifically categorized
def is_home(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['home']
            break
    return output


# check if the video is specifically categorized
def is_mom(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['mom']
            break
    return output


# check if the video is specifically categorized
def is_dp(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['dp']
            break
    return output


def is_bdsm(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['dp']
            break
    return output


def is_milf(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['milf']
            break
    return output


def is_orgy(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['orgy']
            break
    return output


def is_casting(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['casting']
            break
    return output


def is_massage(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['massage']
            break
    return output


def is_parody(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['parody']
            break
    return output

def is_only_head(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = 0
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['only_head']
            break
    return output

# get duration and quality from the database
def get_duration_and_quality(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output1 = ''
    output2 = ''
    for i in range(len_db):
        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output1 = db_preloaded[i]['duration']
            output2 = db_preloaded[i]['quality']
            break
    return output1, output2


# get the site from the database
def get_site(id_entry, id_video, db_preloaded):
    len_db = len(db_preloaded)
    output = ''
    for i in range(len_db):

        if db_preloaded[i]['id_entry'] == id_entry and db_preloaded[i]['id_video'] == id_video:
            output = db_preloaded[i]['studio']
            break
    output = output.replace('.com', '')
    if output == '':
        output = 'unknown'
    return output


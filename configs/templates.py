from blocks import global_var as gv

size_of_font = str(gv.getv('size_of_font'))

# html oftenly used unchanged part of code
style_list_string = '''<style>
\n.container {\n
    position: relative;\n
    text-align: center;\n
    color: white;\n
}\n\n
.top-left {\n
    position: absolute;\n
    top: 8px;\n
    left: 16px;\n
    background-color: rgba(0,0,0,.5);\n
    font-weight: bold;\n
    font-size: 70px;\n
}\n
.top-right {\n
    position: absolute;\n
    top: 8px;\n
    right: 16px;\n
    background-color: rgba(0,0,0,.5);\n
    font-weight: bold;\n
    font-size: 40px;\n
}\n\n
.bottom-right {\n
    position: absolute;\n
    bottom: 8px;\n
    right: 16px;\n
}\n\n
.centered {\n
    position: absolute;\n
    top: 50%;\n
    left: 50%;\n
    transform: translate(-50%, -50%);\n
}\n

.fcc-btn {\n
    background-color: red;\n
    color: white;\n
    padding: 15px 25px;\n
    text-decoration: none;\n
    font-size: 75px
}\n
.fcc-btn-inactive {\n
    background-color: grey;\n
    color: black;\n
    padding: 15px 25px;\n
    text-decoration: none;\n
    font-size: 75px
}\n

</style>\n'''

style_string_color = '''<style>\n
    .purpleText\n
    {\n
        color:purple;\n
        #font-weight:bold;\n
        font-size: ''' + size_of_font + '''px;\n
        font-family:monospace\n
    }\n
    .redText\n
    {\n
        color:red;\n
        font-weight:bold;\n
        font-size: ''' + size_of_font + '''px;\n
        font-family:monospace\n
    }\n
    .greenText\n
    {\n
        color:green;\n
        #font-weight:bold;\n
        font-size: ''' + size_of_font + '''px;\n
        font-family:monospace\n

    }\n
    .blackText\n
    {\n
        color:black;\n
        #font-weight:bold;\n
        font-size: ''' + size_of_font + '''px;\n
        font-family:monospace\n

    }\n
</style>\n'''

# 3 parts of cat file
cat_1_3 = '''<html>
<head>
<title> Insertion </title>
<style>
    body{
        background-color: lightblue:
    }
    .data input{
        width: 40%:
        margin-top: 1%;
        padding:1%;
        border: 0.5px solid blue;
        border-radius: 50px;
    }
    .bata input{
        width: 40%:
        margin-top: 1%;
        padding:1%;
        border: 10.5px solid red;
        border-radius: 50px;
    }
</style>
</head>
<body>
<center>
    <h1> Insertion </h1>
<form action = "" method = "POST">
    <div class = "data">'''
cat_2_3 = '''
    </div>
    </form>
    </center>'''
cat_3_3 = '''
if (isset($_POST['likes']))
{
    $result_query = "SELECT `likes` FROM `categories` WHERE `id_video` = '$id_video' AND `id_entry` = '$id_entry'";
    $result = mysqli_query($connection, $result_query);
    $query1 = "UPDATE categories SET likes = '0'  WHERE id_video = '$id_video' AND id_entry = '$id_entry'";
    $query0 = "UPDATE categories SET likes = '1'  WHERE id_video = '$id_video' AND id_entry = '$id_entry'";
    $row = $result->fetch_assoc(); 
    $query2 = "INSERT INTO categories_old (`id_entry`,`id_video`) VALUES('$id_entry','$id_video')";
    $query_run = mysqli_query($connection, $query2);
    if ($row['likes'] == 0)
    {
        $query_run = mysqli_query($connection, $query0);
        if ($query_run)
        {
            echo '<script> alert("liked") </script>';
        }
        else
        {
            echo '<script> alert("Data not Inserted") </script>';
        }
    }
    else
    {
        $query_run = mysqli_query($connection, $query1);
        if ($query_run)
        {
            echo '<script> alert("disliked") </script>';
        }
        else
        {
            echo '<script> alert("Data not Inserted") </script>';
        }
    }

}

if (isset($_POST['delete']))
{
    $query2 = "INSERT INTO categories_delete (`id_entry`,`id_video`) VALUES('$id_entry','$id_video')";
    $query_run = mysqli_query($connection, $query2);
    if ($query_run)
    {
        echo '<script> alert("delete_pull_created") </script>';
    }
    else
    {
        echo '<script> alert("Data not Inserted") </script>';
    } 
}

?>'''

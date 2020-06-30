<?php

if (isset($_GET["album"])) {
    $album = $_GET["album"];
} else {
    echo "<p class='warning'><strong>";
    echo "No Specified album";
    echo "</strong></p>";
    exit(0);
}
$link = mysqli_connect("121.199.77.180:3306", 'root', 'Zrh999999', 'NeteaseCloudMusic');

# 设定字符集
$link->set_charset("utf8");
# 执行SQL语句
$result1 = mysqli_query($link, "SELECT * from Albums where name='$album'");
# 检测返回结果
if ($result1) {
    $infos = mysqli_fetch_array($result1);
    $ID = $infos["id"];
    $album_name = $infos["name"];
    $album_url = $infos["url"];
    $songs = $infos["songs"];
    $total_com = $infos["album comments"];
    $cover = $infos["cover"];
    $introduction = mb_substr($infos['introduction'], 0, 500);

    $songs = explode(',', $songs);
    $len = count($songs);
    foreach ($songs as $key => $value) {
        $value = substr($value, 2, -1);
        $songs[$key] = $value;
    }
    $songs[$len - 1] = substr($songs[$len - 1], 0, -1);
} else {
    echo "404 NOT FOUND!<br>";
    exit(0);
}
?>


<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>iCrescendo-<?php echo $album_name ?></title>
    <!-- 引入 echarts.js -->
    <script src="echarts.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/album_visualization.css" />
    <style>
        body {
            background-color: antiquewhite;
        }

        .bkg {
            background-image: url(album.jpg);
            background-position: center;
            background-repeat: no-repeat;
            background-size: 120%;
            border-radius: 50%;
            width: 300px;
            height: 300px;
            position: absolute;
            top: 230px;
            left: 700px;
        }

        .pic {
            <?php
            echo "background-image: url('" . $cover . "');";
            ?> 
            background-position: center;
            background-repeat: no-repeat;
            background-size: 100%;
            border-radius: 50%;
            position: absolute;
            top: 280px;
            left: 750px;
            width: 200px;
            height: 200px;
        }

        .intro {
            position: absolute;
            top: 550px;
            left: 450px;
            width: 800px;
            height: 800px;
        }
    </style>
</head>

<body>
    <nav class="codrops-demos" style="position: absolute; left: 400px; top: 5px;">
        <p style="font-size: 20px;">&nbsp;&nbsp;&nbsp;Please choose one type to search</p>
        <a style="font-size: 25px; text-decoration:underline;" href="../../ranking_of_singers/index.html">singers</a>
        <a style="font-size: 25px; text-decoration:underline;" href="../index.html">albums</a>
        <a style="font-size: 25px; text-decoration:underline;" href="../../ranking_of_songs/index.html">songs</a>
        <form target="_self" style="position: absolute; left: 600px; top: 70px; font-size: 20px;" method="GET" action="../../search/search_album.php">
            <input style="font-size: 20px;" type="text" class="search-input" placeholder="          Type to search" name="album" />
            <input type="submit" class="search-submit" value=" ">
        </form>
    </nav><br><br><br><br><br><br>
    <?php
    // echo "<h1>" .$album_name ."</h><br><br>";
    // echo "<br><a style='font-size: 20px; position:absolute; left:46%; top:80px; color:black; text-decoration: none;' href='".$album_url."'>know more!</a>"
    echo "<p style='font-size:30px;'>Album: ";
    echo "<a style='text-decoration:underline; color:black;' target='_blank' href='" . $album_url . "'>";
    echo $album_name;
    echo "</a></p><br>";
    ?>
    <div class="bkg"></div>
    <div class="pic"></div>
    <div class="intro">
        <h1>专辑简介：</h1>
        <p>
            <?php
            echo $introduction;
            ?>
        </p>
    </div>

    <div id="pie" style="position: absolute; left: 100px; top: 900px ; width: 1500px;height:650px;"></div>
    <script type="text/javascript">
        var myPieChart = echarts.init(document.getElementById('pie'));

        option = {
            title: {
                text: '本专辑中各歌曲影响力占比',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                bottom: 10,
                left: 'center',
                data: [

                    <?php
                    for ($i = 0; $i < $len; $i++) {
                        $j = $i + 1;
                        $temp = mysqli_query($link, "SELECT * from Songs where id='$songs[$i]'");
                        if ($temp) {
                            $infos = mysqli_fetch_array($temp);
                            echo "'" . $infos['name'] . "',";
                        }
                    }
                    ?>
                ]
            },
            series: [{
                type: 'pie',
                radius: '65%',
                center: ['50%', '50%'],
                selectedMode: 'single',
                data: [

                    <?php
                    for ($i = 0; $i < $len; $i++) {
                        $j = $i + 1;
                        $temp = mysqli_query($link, "SELECT * from Songs where id='$songs[$i]'");
                        if ($temp) {
                            $infos = mysqli_fetch_array($temp);
                            echo "{value: " . $infos['commentnum'] . ", name: '" . $infos['name'] . "'},";
                        }
                    }
                    ?>
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        myPieChart.setOption(option);
    </script>

</body>

</html>
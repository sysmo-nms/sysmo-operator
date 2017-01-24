<?php
    $token = $_GET['token'];
    $ch = curl_init('https://api.opensuze.org/trigger/runservice');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array("Authorization: $token"));
    curl_exec($ch);
    $info = curl_getinfo($ch)['http_code'];
    $code = $info['http_code'];
    header("HTTP/1.1 $code Bla");
    exit();
?>

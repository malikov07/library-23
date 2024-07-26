<?php
$username = 'admin123';
$password = '12345678';

$getedUsername = $_POST['username'];
$getedPassword = $_post['password'];

if($getedUsername == $username && $getedPassword == $password){
    header("Location: ../../pages/library.html");
}




?>
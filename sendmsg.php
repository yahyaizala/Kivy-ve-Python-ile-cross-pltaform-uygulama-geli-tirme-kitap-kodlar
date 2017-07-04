<?php

/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
header('Content-Type: application/json; charset=utf-8');
function connection()
{
$host="localhost";
$db="1117365";
$username="1117365";
$password="123456";  
    $con=new mysqli($host,$username,$password,$db);
    if($con->connect_error)
        die("{'res':'error'}");
    //die("{'res':'error'}".mysqli_connect_error());
    return $con;
} 
if(isset($_REQUEST["msg"])
        && isset($_REQUEST["id"])
        && isset($_REQUEST["to_id"])
        &&isset($_REQUEST["tm"]))
{
    $msg=$_REQUEST["msg"];
    $id=$_REQUEST["id"];
    $to_id=$_REQUEST["to_id"];
    $tm=$_REQUEST["tm"];
    $read="y";
    $con=  connection();
    if(isset($_REQUEST["uniq"]))
    {
        $uniq=$_REQUEST["uniq"];
        $sql="INSERT INTO  messages ( user_id , to_id ,  msg ,  tm , readed,uniq_s )"
            ."VALUES ('$id',  '$to_id',  '$msg',  '$tm', '$read','$uniq')";	
    $result=  mysqli_query($con,$sql);
    if ($result) {
        echo '{"res":"success"}';
    } else {
        echo '{"res":"error"}';
    }
        
        
    }
 else {
        $uniq=md5(uniqid(rand(), true));        
        $sql="INSERT INTO  messages ( user_id , to_id ,  msg ,  tm , readed,uniq_s )"
            ."VALUES ('$id',  '$to_id',  '$msg',  '$tm', '$read','$uniq')";	
    $result=mysqli_query($con,$sql);   
    if($result)
    {
       
        echo '{"res":"success","uniq":"'.$uniq.'"}'; 
    }
    else
    {
         echo '{"res":"error"}';
    } 
     
     
     
 }
    
    
    
    
}
else if(isset ($_REQUEST["user_id"]) and isset($_REQUEST["to_id"]))
{
    
    $user_id=$_REQUEST["user_id"];
    $to_id=$_REQUEST["to_id"];
    $con=  connection();
    $sql="select uniq_s from messages where (user_id='$user_id' and to_id='$to_id') or (user_id='$to_id' and to_id='$user_id')";
    $result=  mysqli_query($con,$sql);
    if($result)
    {
       $row=  mysqli_fetch_assoc($result);
    if($row)
        echo '{"uniq":"'.$row["uniq_s"].'"}';  
    else
    {
     echo '{"uniq":"not_yet_set"}';   
    }
    }
    else
    {
       echo '{"uniq":"not_yet_set"}';   
    }
   
    
}
else
{
    echo '{"res":"error"}';
}

?>
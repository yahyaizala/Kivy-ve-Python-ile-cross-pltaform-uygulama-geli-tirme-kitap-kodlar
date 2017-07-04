<?php 
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


if(isset($_POST["user"])&& isset ($_POST["psw"]))
{
    
    $con=connection();   
    $user=$_REQUEST["user"];
    $psw=$_REQUEST["psw"];            
    $sql="SELECT  `id` ,  `user` FROM  `loggers` WHERE  `email` =  '$user' AND  `psw` =  '$psw'";	
    $res=  mysqli_query($con,$sql);
   $json='{"res":"success","data":[';
    $fs=true;
    while($row=  mysqli_fetch_assoc($res))
     {          
       if ($fs)
       {
           $data='{"id":"'.$row["id"].'","user":"'.$row["user"].'"}';
           $fs=false;
           
       }else
       {
         $data=',{"id":"'.$row["id"].'","user":"'.$row["user"].'"}'; 
       }        
        $json.=$data;      
      
         
    }    
        
    $json .=']}';
    echo $json;
    


  
}
else if(isset ($_REQUEST["list"]))
{   
    $con=connection();
    $sql="select id,user,img from loggers";
    $res=  mysqli_query($con,$sql);  
    $json='{"res":"success","data":[';
    $fs=true;
    while($row=  mysqli_fetch_assoc($res))
     {          
       if ($fs)
       {
           $data='{"id":"'.$row["id"].'","user":"'.$row["user"].'","img":"'.$row["img"].'"}';
           $fs=false;
           
       }else
       {
          $data=',{"id":"'.$row["id"].'","user":"'.$row["user"].'","img":"'.$row["img"].'"}';
       }        
        $json.=$data;        
         
    }            
        
    $json .=']}';
    echo $json;     
            
  }//giris
  else if(isset ($_REQUEST["user_id"]) && isset ($_REQUEST["to_id"]))
  {
      $user_id=$_REQUEST["user_id"];
      $to_id=$_REQUEST["to_id"];
      $con=  connection();
      $uniq=-1;
      $sql="select uniq_s from messages where (user_id='$user_id' and to_id='$to_id') or (user_id='$to_id' and to_id='$user_id')";   
      $result= mysqli_query($con,$sql);
      $rowi = mysqli_fetch_assoc($result);
    if ($rowi) {
        $uniq = $rowi["uniq_s"];
        $sql="select uniq_s,msg,tm,user_id from messages where uniq_s='$uniq' order by tm";
        $result=  mysqli_query($con,$sql);
        $json = '{"res":"success","data":[';
        $fst = true;
        while ($row = mysqli_fetch_assoc($result)) {


            if ($fst) {
                $data = '{"uniq":"'.$row["uniq_s"].'","msg":"' . $row["msg"] . '","time":"' . $row["tm"] . '","user_id":"' . $row["user_id"] . '"}';
                $fst = false;
            } else {
                $data = ',{"uniq":"'.$row["uniq_s"].'","msg":"' . $row["msg"] . '","time":"' . $row["tm"] . '","user_id":"' . $row["user_id"] . '"}';
            }
            $json.=$data;
        }  
        $json .=']}';
        echo $json;
    } else {
        echo '{"res":"no_uniq"}';
        
    }
}//surekli
    else if(isset ($_REQUEST["user_id"]) && isset ($_REQUEST["uniq"]))
  {
      $user_id=$_REQUEST["user_id"];    
      $uniq=$_REQUEST["uniq"];   
      $con=  connection();
      $sql="SELECT  id,user_id, msg ,tm FROM  messages WHERE to_id='$user_id' and uniq_s='$uniq' and readed='y' order by tm";        
      $result=  mysqli_query($con,$sql);         
     $json='{"res":"success","data":[';
     $fst=true; 
     $ids=array();     
    while($row=mysqli_fetch_assoc($result))
     {   
      $data="";     
        
     if ($fst)
     {         
      $data='{"msg":"'.$row["msg"].'","time":"'.$row["tm"].'","user_id":"'.$row["user_id"].'"}'; 
      $fst=false;
      }
      else
      {
          $data=',{"msg":"'.$row["msg"].'","time":"'.$row["tm"].'","user_id":"'.$row["user_id"].'"}'; 
        
      }   
      
        $json .=$data; 
        $ids[]=$row["id"];
        
     
          
    }
    
    $json .=']}';
    echo $json;     
    foreach ($ids as $key=>$value)
    {
         $sql="update messages set readed='e' where id='$value'";
         mysqli_query($con,$sql);
    }   
    
    
        
  }
      
 





 ?>




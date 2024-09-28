<?php
{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;\f1\fnil\fcharset0 Menlo-Bold;}
{\colortbl;\red255\green255\blue255;\red38\green38\blue38;\red242\green242\blue242;\red255\green255\blue255;
\red77\green179\blue214;\red0\green0\blue255;\red206\green60\blue62;\red77\green173\blue74;}
{\*\expandedcolortbl;;\cssrgb\c20000\c20000\c20000;\cssrgb\c96078\c96078\c96078;\cssrgb\c100000\c100000\c100000;
\cssrgb\c35686\c75294\c87059;\cssrgb\c0\c0\c100000;\cssrgb\c85098\c32549\c30980;\cssrgb\c36078\c72157\c36078;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 $myCheck["service"] = 
\f1\b\fs19\fsmilli9750 \cf4 \cb5 \strokec4 0
\f0\b0\fs26 \cf2 \cb3 \strokec2 ;\cb1 \
\cb3 $myCheck["imei"] = "
\f1\b\fs19\fsmilli9750 \cf4 \cb5 \strokec4 000000000000000
\f0\b0\fs26 \cf2 \cb3 \strokec2 ";\cb1 \
\cb3 $myCheck["key"] = "
\f1\b\fs19\fsmilli9750 \cf4 \cb5 \strokec4 5PZ-WHH-FYC-IT1-EZ9-L9L-ZHV-R1Y
\f0\b0\fs26 \cf2 \cb3 \strokec2 ";\
$ch = curl_init("\cf6 \ul \ulc6 \strokec6 https://api.ifreeicloud.co.uk\cf2 \ulnone \strokec2 ");\cb1 \
\cb3 curl_setopt($ch, CURLOPT_POSTFIELDS, $myCheck);\cb1 \
\cb3 curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);\cb1 \
\cb3 curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);\cb1 \
\cb3 curl_setopt($ch, CURLOPT_TIMEOUT, 60);\cb1 \
\cb3 $myResult = json_decode(curl_exec($ch));\cb1 \
\cb3 $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);\cb1 \
\cb3 curl_close($ch);\
if($httpcode != 200) \{\cb1 \
\cb3 \'a0\'a0\'a0\'a0echo "
\f1\b\fs19\fsmilli9750 \cf4 \cb7 \strokec4 Error: HTTP Code $httpcode
\f0\b0\fs26 \cf2 \cb3 \strokec2 ";\cb1 \
\cb3 \} elseif($myResult->success !== true) \{\cb1 \
\cb3 \'a0\'a0\'a0\'a0echo "
\f1\b\fs19\fsmilli9750 \cf4 \cb7 \strokec4 Error: $myResult->error
\f0\b0\fs26 \cf2 \cb3 \strokec2 ";\cb1 \
\cb3 \} else \{\cb1 \
\cb3 \'a0\'a0\'a0\'a0echo 
\f1\b\fs19\fsmilli9750 \cf4 \cb8 \strokec4 $myResult->response
\f0\b0\fs26 \cf2 \cb3 \strokec2 ;\cb1 \
\cb3 \'a0\'a0\'a0\'a0echo "<hr><pre>".print_r(
\f1\b\fs19\fsmilli9750 \cf4 \cb5 \strokec4 $myResult->object
\f0\b0\fs26 \cf2 \cb3 \strokec2 , true)."</pre><hr>"; // TEST ONLY\cb1 \
\cb3 \'a0\'a0\'a0\'a0// Here you can access specific info!\cb1 \
\cb3 \'a0\'a0\'a0\'a0// echo $myResult->object->model;\cb1 \
\cb3 \}\
}
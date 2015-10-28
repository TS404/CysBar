<?php

function san_jobid($j) {
    // removes any non lowercase hex letters
    return preg_replace('/[^0-9a-f]/', '', $j);
}

function san_c($c) {
    // returns shell excaped integer value (or 0)
    if (is_numeric($c)) {
        $c = intval($c);
        if ($c >= 0) {
            return $c;
        }
    }
    return 0;
}
function san_barcode($b) {
    // only accept letters
    $b = preg_replace('/[^a-zA-Z]/', '', $b);
    //$b = substr($b, 0, 12);
    return $b;
}
function san_seq($s) {
    
    // fix EOL chars
    $s = str_replace("\r\n","\n",$s);
    $s = str_replace("\r","\n",$s);
    
//TODO: sanitise inputfa
    return $s;
}

function getKey($a, $k, $d) {
    if (array_key_exists($k, $a)) {
        return $a[$k];
    }
    return $d;
}
function popKey(&$a, $k, $d) {
    if (array_key_exists($k, $a)) {
        $v = $a[$k];
        unset($a[$k]);
        return $v;
    }
    return $d;
}
function popKey2(&$a, $k, $d) {
    if (array_key_exists($k, $a) && $a[$k] != "") {
        $v = $a[$k];
        unset($a[$k]);
        return $v;
    }
    return $d;
}
function saveVars(&$s, $c, $bc, $seq) {
    $s['c1'] = $c[0];
    $s['c2'] = $c[1];
    $s['c3'] = $c[2];
    $s['c4'] = $c[3];
    $s['c5'] = $c[4];
    $s['c6'] = $c[5];
    $s['c7'] = $c[6];
    $s['c8'] = $c[7];
    $s['bc1'] = $bc[0];
    $s['bc2'] = $bc[1];
    $s['bc3'] = $bc[2];
    $s['bc4'] = $bc[3];
    $s['bc5'] = $bc[4];
    $s['bc6'] = $bc[5];
    $s['bc7'] = $bc[6];
    $s['bc8'] = $bc[7];
    $s['seq'] = $seq;
}

?>

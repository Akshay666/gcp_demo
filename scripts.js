function analyze_button_func()
{

  var form_submission = document.getElementById("form_fill");
  var text = form_submission.elements[0].value;

  var e = document.getElementById("dropdown_selection");
  var target_language_coded = e.value

  console.log('Here is the target language coded',target_language_coded);
  console.log('Here is the text you entered:', text);

  $.ajax({
    url : '/translate',
    method : 'POST',
    data: JSON.stringify({text_to_translate:text,target_lang:target_language_coded}),
    success: function(res)
    {
      document.getElementById("translated_text").innerHTML = res;

    }
  })


}

function customer_button_func()
{
  var form_submission = document.getElementById("c1_form_fill");
  var text = form_submission.elements[0].value;

  document.getElementById("customer_textbox").innerHTML += 'You: ' + text + '<br />';  // Show the customer what they typed as it is
  document.getElementById("rep_text").innerHTML += 'Original text: ' + text + '<br />'; // Show the representative what the customer typed, as it is
  console.log('this is text entered by the customer', text);

  $.ajax({
    url : '/detect',
    method : 'POST',
    data: JSON.stringify(text),
    success: function(res)
    {
      console.log('this is the detected language from the customer', res);
      document.getElementById("detected_language").innerHTML += res; // Show the customer representative which language the customer is typing in
    }
  })

  target_language = 'en';

  $.ajax({
    url : '/translate',
    method : 'POST',
    data: JSON.stringify({text_to_translate:text,target_lang:target_language}), // Translate the customer's message to English for the representative
    success: function(res)
    {
      document.getElementById("rep_text").innerHTML += 'Translated text: ' + res + '<br />'; // Show the rep the translated version of the customer's text
    }
  })

}

function rep_button_func()
{
  var form_submission = document.getElementById("rep_form_fill");
  var rep_reply = form_submission.elements[0].value;

  document.getElementById("rep_text").innerHTML += 'You: ' + rep_reply + '<br />'; // Show the representative the original version of their reply

  target_language = (document.getElementById("detected_language").innerHTML).slice(-2);

  console.log('this is the text rep entered', rep_reply);
  console.log('this is the detected language from the customer', target_language);

  $.ajax({
    url : '/translate',
    method : 'POST',
    data: JSON.stringify({text_to_translate:rep_reply,target_lang:target_language}),
    success: function(res)
    {
      document.getElementById("customer_textbox").innerHTML += 'HelpDesk: ' + res + '<br />';

    }
  })
}

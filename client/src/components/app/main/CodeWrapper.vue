<template>
    <div class="panel left"> 
        <li class="divider"></li>
        <div class="subpanel first">
            <textarea id="id_html" name="html" placeholder="HTML"></textarea>  
        </div>
        <li class="divider"></li>
        <div class="subpanel second"> 
            <textarea id="id_css" name="css" placeholder="CSS"></textarea>
        </div>
        <li class="divider"></li>
        <div class="subpanel third">
            <textarea id="id_javascript" name="javascript" placeholder="JavaScript"></textarea>
        </div>
    </div>
    <div class="v-line"></div>
    <div class="panel right">
        <li class="divider"></li>
        <div class="subpanel result"> 
            <iframe name="result" allow="midi; geolocation; microphone; camera; display-capture; encrypted-media; clipboard-read; clipboard-write; notifications; payment-handler; persistent-storage; background-sync; ambient-light-sensor; accessibility-events;" sandbox="allow-modals allow-forms allow-scripts allow-same-origin allow-popups allow-top-navigation-by-user-activation allow-downloads" allowfullscreen="false" allowpaymentrequest="" frameborder="0" src=""></iframe>
        </div>
    </div>
</template>
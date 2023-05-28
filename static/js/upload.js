$(document).ready(function(){
    document.querySelector("#getFile").onchange = function(){
    document.querySelector("#file-name").textContent = this.files[0].name;
    }
});

var msg='';
function onDeleteButton(){
	msg='您確定要刪除?';
}
function onUpdateButton(){
	msg='您確定要修改?';
}
function onUploadButton()
{
	msg='您確定要上傳影片? 若已有相同檔名影片會將其覆蓋';
}
function checkSubmit(){			
	if(confirm(msg)){
			document.getElementById("wait").style.display = "block";
			document.getElementById("fin").style.display = "none";
			return true;
		}
		else{
			return false;
    }   
}
//a simple fix to compatible modern browsers
var hasCommitted

function Forward()
{
   window.history.forward(1);
   // Redirects if the next page exists,
   // including the post-back versions.
}

// JScript File
function CheckInputString()
{
  if ((event.keyCode > 32 && event.keyCode < 46) || event.keyCode==47 || (event.keyCode > 57 && event.keyCode < 64) || (event.keyCode > 90 && event.keyCode < 95) || event.keyCode==96 ) event.returnValue = false;
}

function isNumberic(str) {
	return /^\+?\d+(\.\d+)?$/.test(str);
}

function SwitchMenu(obj){
	if(document.getElementById){
		var el = document.getElementById(obj);
		var ar = document.getElementById("masterdiv").getElementsByTagName("span");
		if(ar != null) 
		{
			for (var i=0; i<ar.length; i++)
			{
			   if (ar[i].className=="submenu")
			   ar[i].style.display = "none";
			}
			if(el != null)
			{
				if(el.style.display != "block")
				{			        
					el.style.display = "block";
				}
				else
				{
					el.style.display = "none";
				}
			}
		}
	}
}
function changebar(a){
	for (var i=1;i<=4;i++){
		eval("menu"+i).style.display="none";
		eval("content"+i).style.display="none";
	}
	eval("menu"+a).style.display="block";
	eval("content"+a).style.display="block";
}
function DropDownListSelected(targ,selObj,restore){ 
	eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
	if (restore)
		selObj.selectedIndex=0;
}
function getvalue(){
  alert(document.all['txtMenu'].value);
}
function ChangeMenu(menuValue) { //v3.0
  document.all('txtMenu').value = menuValue;   
}
function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
	var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
	if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
	d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}
function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}
function dyniframesize() 
 {
  var dyniframe=new Array()
  for (i=0; i<iframeids.length; i++)
  {
   if (document.getElementById)
   {
	//自动调整iframe高度
	dyniframe[dyniframe.length] = document.getElementById(iframeids[i]);
	if (dyniframe[i] && !window.opera)
	{
	 dyniframe[i].style.display="block"
	 if (dyniframe[i].contentDocument && dyniframe[i].contentDocument.body.offsetHeight) 
	 {
	 //如果用户的浏览器是NetScape
		if(dyniframe[i].contentDocument.body.offsetHeight < 464)
			 dyniframe[i].height = 464 ;
		  else
			 dyniframe[i].height = dyniframe[i].contentDocument.body.offsetHeight; 
	  }
	 else if (dyniframe[i].Document && dyniframe[i].Document.body.scrollHeight) 
	 //如果用户的浏览器是IE
	 {   
		  if(dyniframe[i].Document.body.scrollHeight < 464)
			 dyniframe[i].height = 464 ;
		  else
			 dyniframe[i].height = dyniframe[i].Document.body.scrollHeight;
	  }
	}
   }
   //根据设定的参数来处理不支持iframe的浏览器的显示问题

   if ((document.all || document.getElementById) && iframehide=="no")
   {
	var tempobj=document.all? document.all[iframeids[i]] : document.getElementById(iframeids[i])
	tempobj.style.display="block"
   }
  }
 }
 
 
 
 //显示模态窗口
function showModal(path) {
  window.showModalDialog(path,window,"status:no;scroll:no;dialogHeight:600px;resizable:yes;help:no;dialogWidth:800px;dialogTop:80px;dialogLeft:150px");	
}
//显示非模态窗口
function showNormalDialog(path)
{
  window.open(path);
} 
//根据参数改变Menu的Iframe显示的页面。
function iframeContent(iframeId1,iframeSrc1,iframeId2,iframeSrc2) 
{ 
  var iframe1 = document.getElementById(iframeId1); 
  iframe1.src = iframeSrc1; 
  var iframe2 = document.getElementById(iframeId2); 
  iframe2.src = iframeSrc2; 
  
} 

//根据左边的菜单的点击，改变右边Iframe显示的页面地址。
function iframeRightContent(iframeId1,iframeSrc1) 
{ 
  var iframe1 = parent.document.getElementById(iframeId1); 
  iframe1.src = iframeSrc1;
  iframe1.contentWindow.location.replace('http://lab.hnist.cn/pec2011/Web/CourseSel/'+iframeSrc1);
}

//关闭模态窗口
function closeWin() 
{
  parent.window.close();
}

//从Request中取得指定参数的值
function getvalue(name)
{
	var str=window.location.search;
	if (str.indexOf(name)!=-1)
	{
	var pos_start=str.indexOf(name)+name.length+1;
	var pos_end=str.indexOf("&",pos_start);
	if (pos_end==-1)
	  {
		return str.substring(pos_start);
	  }
	else
	  {
		return str.substring(pos_start,pos_end)
	  }
	}
	else
	  {
		return null;
	  }
}

//动态的改变iframe的高度
function iframeHeight() {
  var iframeMain = parent.document.getElementById("Main"); 
  var iframeMainleft =parent.document.getElementById("leftMenu"); 
  if (iframeMain.scrollHeight < 700) {
	iframeMain.height="700";
	iframeMainleft.height="700";
  } else {
    
	iframeMain.height=iframeMain.Document.body.scrollHeight;
	iframeMainleft.height=iframeMain.Document.body.scrollHeight;
	
  }
  window.history.forward(1);

}

//BBS页面动态的改变iframe的高度
function iframeHeightleft() {
  
  var iframeMain = parent.document.getElementById("Main"); 
  var iframeMainleft =parent.document.getElementById("leftMenu"); 
  var tableheight=0;
  if (iframeMainleft.contentWindow.document.all.GVForumList != null) {
     tableheight=iframeMainleft.contentWindow.document.all.GVForumList.offsetHeight;
  }
  if(tableheight < 700 ) {
    if(iframeMain.scrollHeight < 700) {
    iframeMain.height="700";
	iframeMainleft.height="700";
	} else {
	iframeMain.height = iframeMain.Document.body.scrollHeight;
	iframeMainleft.height= iframeMain.Document.body.scrollHeight;
	}
  } else if (iframeMain.Document.body.scrollHeight < tableheight) {
    iframeMain.height=tableheight;
	iframeMainleft.height=tableheight;
  } else {
    iframeMain.height=iframeMain.Document.body.scrollHeight;
	iframeMainleft.height=iframeMain.Document.body.scrollHeight;
  }
}


//动态的改变iframe的高度
function iframeSizeSubWin() {
//  var iframeMain = parent.document.getElementById("modalFrame"); 
//  if (iframeMain.Document.body.scrollHeight < 250) {
//    iframeMain.height="250";
//  } else {
//    iframeMain.height=iframeMain.Document.body.scrollHeight;
//  }
//  if (iframeMain.Document.body.scrollWidth < 350) {
//    iframeMain.Width="350";
//  } else {
//   iframeMain.height=iframeMain.Document.body.scrollWidth;
//  }
}
  
//删除警告
function DeleteAlert()
{
	return confirm('真的要删除吗？');
}

//退选警告
function QuitSelectAlert()
{
	return confirm('真的要退选吗？');
}
  
//PEC06041删除警告
function DeleteAlert_PEC06041()
{
	return confirm('如果删除实验课程,请确认此实验课程无学生选课！！！');
}

//判断复选框是否被选中.
function ButtonAlert(chk,id){
 var oEvent = document.all(id);
 var chks = oEvent.getElementsByTagName("INPUT");
 var count=0;
 for(var i=0; i<chks.length; i++)
 {
   if(chks[i].type=="checkbox" && chks[i].checked==true)
   count++;
 }
 if(count>0)
 {
   return confirm('你确认删除吗？');
 } else
 {
   alert('最少选择一项');
   return false;
 }
} 
//上传视频文件类型检查
function CheckMovieFileType(type)
{
	if(type == null && type == "")
	{
	  alert("请选择上传的文件");
	  return false;
	} 
	else 
	if (type.length < 4)
	{
	  alert("请上传avi或asf或mpg或wma或swf或mpeg或jpeg或ram或rmm或ra或rm或rp或rt格式的文件！");
	  return false;
	} 
	else
	  if((type.substring(type.length-5).toUpperCase()!=".MPEG") && (type.substring(type.length-5).toUpperCase()!=".JPEG") && 
	     (type.substring(type.length-4).toUpperCase()!=".AVI")  && (type.substring(type.length-4).toUpperCase()!=".ASF")&&
	     (type.substring(type.length-4).toUpperCase()!=".MPG")  && (type.substring(type.length-4).toUpperCase()!=".WMA")&&
	     (type.substring(type.length-4).toUpperCase()!=".SWF")  && (type.substring(type.length-4).toUpperCase()!=".RAM")&&
	     (type.substring(type.length-4).toUpperCase()!=".RMM")  && (type.substring(type.length-3).toUpperCase()!=".RM")&&
	     (type.substring(type.length-3).toUpperCase()!=".RA")   && (type.substring(type.length-3).toUpperCase()!=".RP")&&
	     (type.substring(type.length-3).toUpperCase()!=".RT"))
	   {
	    alert("请上传avi或asf或mpg或wma或swf或mpeg或jpeg或ram或rmm或ra或rm或rp或rt格式的文件！");
	     return false;
	   }
	
	
	return true;
}
//上传讲座文件类型检查
function CheckWordFileType(type)
{
	if(type == null && type == "")
	{
	  alert("请选择上传的文件");
	  return false;
	} else if (type.length < 4)
	{
	  alert("请上传doc或ppt格式的讲座！");
	  return false;
	} else if((type.substring(type.length-4).toUpperCase()!=".DOC")&&(type.substring(type.length-4).toUpperCase()!=".PPT"))
	{
	  alert("请上传doc或ppt格式的讲座！");
	  return false;
	}
	return true;
}
//上传仿真实验文件类型检查
function CheckZIPFileType(type)
{
	if(type == null && type == "")
	{
	  alert("请选择上传的文件");
	  return false;
	} else if (type.length < 4)
	{
	  alert("请上传zip或rar格式的文件！");
	  return false;
	} else if((type.substring(type.length-4).toUpperCase()!=".ZIP")&&(type.substring(type.length-4).toUpperCase()!=".RAR"))
	{
	  alert("请上传zip或rar格式的文件！");
	  return false;
	}
	return true;
}


function NowDateView()
{
   var  bsYear;
var  bsDate;
var  bsWeek;
var  arrLen=8;	//数组长度
var  sValue=0;	//当年的秒数
var  dayiy=0;	//当年第几天
var  miy=0;	//月份的下标
var  iyear=0;	//年份标记
var  dayim=0;	//当月第几天
var  spd=86400;	//每天的秒数

var  year1999="30;29;29;30;29;29;30;29;30;30;30;29";	//354
var  year2000="30;30;29;29;30;29;29;30;29;30;30;29";	//354
var  year2001="30;30;29;30;29;30;29;29;30;29;30;29;30";	//384
var  year2002="30;30;29;30;29;30;29;29;30;29;30;29";	//354
var  year2003="30;30;29;30;30;29;30;29;29;30;29;30";	//355
var  year2004="29;30;29;30;30;29;30;29;30;29;30;29;30";	//384
var  year2005="29;30;29;30;29;30;30;29;30;29;30;29";	//354
var  year2006="30;29;30;29;30;30;29;29;30;30;29;29;30";

var  month1999="正月;二月;三月;四月;五月;六月;七月;八月;九月;十月;十一月;十二月"
var  month2001="正月;二月;三月;四月;闰四月;五月;六月;七月;八月;九月;十月;十一月;十二月"
var  month2004="正月;二月;闰二月;三月;四月;五月;六月;七月;八月;九月;十月;十一月;十二月"
var  month2006="正月;二月;三月;四月;五月;六月;七月;闰七月;八月;九月;十月;十一月;十二月"
var  Dn="初一;初二;初三;初四;初五;初六;初七;初八;初九;初十;十一;十二;十三;十四;十五;十六;十七;十八;十九;二十;廿一;廿二;廿三;廿四;廿五;廿六;廿七;廿八;廿九;三十";

var  Ys=new  Array(arrLen);
Ys[0]=919094400;Ys[1]=949680000;Ys[2]=980265600;
Ys[3]=1013443200;Ys[4]=1044028800;Ys[5]=1074700800;
Ys[6]=1107878400;Ys[7]=1138464000;

var  Yn=new  Array(arrLen);      //农历年的名称
Yn[0]="己卯年";Yn[1]="庚辰年";Yn[2]="辛巳年";
Yn[3]="壬午年";Yn[4]="癸未年";Yn[5]="甲申年";
Yn[6]="乙酉年";Yn[7]="丙戌年";
var  D=new  Date();
var  yy=D.getYear();
var  mm=D.getMonth()+1;
var  dd=D.getDate();
var  ww=D.getDay();
if  (ww==0)  ww="星期日";
if  (ww==1)  ww="星期一";
if  (ww==2)  ww="星期二";
if  (ww==3)  ww="星期三";
if  (ww==4)  ww="星期四";
if  (ww==5)  ww="星期五";
if  (ww==6)  ww="星期六";
ww=ww;
var  ss=parseInt(D.getTime()  /  1000);
if  (yy<100)  yy="19"+yy;

for  (i=0;i<arrLen;i++)
if  (ss>=Ys[i]){
iyear=i;
sValue=ss-Ys[i];        //当年的秒数
}
dayiy=parseInt(sValue/spd)+1;        //当年的天数

var  dpm=year1999;
if  (iyear==1)  dpm=year2000;
if  (iyear==2)  dpm=year2001;
if  (iyear==3)  dpm=year2002;
if  (iyear==4)  dpm=year2003;
if  (iyear==5)  dpm=year2004;
if  (iyear==6)  dpm=year2005;
if  (iyear==7)  dpm=year2006;
dpm=dpm.split(";");

var  Mn=month1999;
if  (iyear==2)  Mn=month2001;
if  (iyear==5)  Mn=month2004;
if  (iyear==7)  Mn=month2006;
Mn=Mn.split(";");

var  Dn="初一;初二;初三;初四;初五;初六;初七;初八;初九;初十;十一;十二;十三;十四;十五;十六;十七;十八;十九;二十;廿一;廿二;廿三;廿四;廿五;廿六;廿七;廿八;廿九;三十";
Dn=Dn.split(";");

dayim=dayiy;

var  total=new  Array(13);
total[0]=parseInt(dpm[0]);
for  (i=1;i<dpm.length-1;i++)  total[i]=parseInt(dpm[i])+total[i-1];
for  (i=dpm.length-1;i>0;i--)
if  (dayim>total[i-1]){
dayim=dayim-total[i-1];
miy=i;
}
bsWeek=ww;
bsDate=yy+"年"+mm+"月";
bsDate2=dd;
bsYear="农历"+Yn[iyear];
bsYear2=Mn[miy]+Dn[dayim-1];
if  (ss>=Ys[7]||ss<Ys[0])  bsYear=Yn[7];

var viewString="<font  color=RED>" + bsDate + bsDate2 + " " + bsWeek + "</font>";
return viewString

}

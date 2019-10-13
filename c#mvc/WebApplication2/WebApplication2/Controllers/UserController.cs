using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using mylogin.Common;


namespace WebApplication2.Controllers
{
    public class UserController : Controller
    {
        public MydbEntities entity = new MydbEntities();
      
        // GET: User
        public ActionResult login()
        {
            return View();
        }
        [HttpPost]
        public ActionResult doLogin(string loginUserName, string loginpasswd)
        {
            
            var mypasswd = pub.Md5Encrypt(loginpasswd);
            var us = entity.usertable.FirstOrDefault(a => a.UserName == loginUserName && a.PassWord == mypasswd);
            if (us != null)
            {
                return Redirect("/Home/Index");
            }
            else
            {
                return Redirect("/User/Login");
            }
        }

    }
}
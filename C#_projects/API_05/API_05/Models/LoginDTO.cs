using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace API_05.Models
{
    public class LoginDTO
    {
        public string Email { get; set; }
        public string Password { get; set; }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace API_05.Models
{
    public enum UserRole
    {
        Admin,
        Customer
    }

    static class UserRoleStringConverter
    {
        public static String GetString(this UserRole role)
        {
            switch (role)
            {
                case UserRole.Admin:
                    return "Admin";
                case UserRole.Customer:
                    return "Customer";
                default:
                    return "None";
            }
        }
    }
}
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Linq;
using System.Reflection;

namespace task02_Generics
{
    public static class Validation 
    {
        public delegate void MyFunction<T>(LstCollection<T> l) where T: BaseClass, new();
        public static string ValidateTitle(string value)
        {
            if (value=="0") return value;
            if (value.Any(char.IsDigit))
            {
                throw new ArgumentException("Title must not contain integers.");
            }
            return value;
        }
        
        public static double ValidatePrice(double value)
        {
            string strValue = value.ToString(CultureInfo.InvariantCulture).
                IndexOf(".", StringComparison.Ordinal) == -1 ? value.ToString(CultureInfo.InvariantCulture) 
                                                               + "." : value.ToString(CultureInfo.InvariantCulture);
            if (strValue.Substring(strValue.IndexOf(".", StringComparison.Ordinal)).Length > 3)
            {
                throw new ArgumentException("Price must have two digits after coma.");
            }
            return value;
        }
        
        public static string ValidateDate(string value)
        {
            if (value == "0") return value;
            DateTime v =DateTime.Parse(value);
            if (DateTime.Compare(DateTime.Now, v) < 0)
            {
                throw new ArgumentException("Non-existent Date.");
            }
            return v.ToString("yyyy-MM-dd");
        }
        
        public static string ValidateDate(string value1, string value2)
        {
            if (value2 == "0") return value2;
            DateTime v1 = DateTime.Parse(value1);
            DateTime v2 = DateTime.Parse(value2);
            if (DateTime.Compare(v1, v2) > 0)
            {
                throw new ArgumentException("Incorrect data, created_at must be lover than updated_at.");
            }
            return ValidateDate(value2);
        }
        
        public static string ValidateImage_url(string value)
        {
            if (value == "0") return value;
            string[] validImageExtensions = { ".jpg", ".jpeg", ".png", ".gif"};
            if (!validImageExtensions.Any(value.EndsWith))
            {
                throw new ArgumentException("Incorrect image_url.");
            }
            return value;
        }
        
        public static string ValidateFile(string value)
        {
            string[] validFileExtensions = { ".txt", ".json"};
            if (!validFileExtensions.Any(value.EndsWith))
            {
                throw new ArgumentException("Incorrect .txt format.");
            }
            return value;
        }
        
        public static List<T> ValidateSearch<T>(List<T> value) where T: BaseClass
        {
            if (value.Count == 0)
            {
                throw new ArgumentException("There's no such elements!");
            }
            return value;
        }
        
        public static PropertyInfo ValidateEdit(PropertyInfo value)
        {
            if (value == null)
            {
                throw new ArgumentException("Wrong Attribute name");
            }
            return value;
        }

        public static void ValidateInput<T>(LstCollection<T> l, MyFunction<T> f) where T: BaseClass, new()
        {
            while (true)
            {
                try
                {
                    f(l);
                    break;
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                    Console.WriteLine("Try one more time!");
                    continue;
                }
            }
        }
    }
}
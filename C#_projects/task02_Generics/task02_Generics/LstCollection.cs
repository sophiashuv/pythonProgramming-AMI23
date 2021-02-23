using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json;

namespace task02_Generics
{
    public class LstCollection<T> where T : BaseClass, new() 
    {
        private List<T> lst;

        public LstCollection() => this.lst = new List<T>();

        public LstCollection(List<T> lst) => this.lst = new List<T>(lst);

        public override string ToString()
        {
            string res = "";
            foreach (T element in lst)
                res += element.ToString() + "\n=\n";
            return "\n" + res.Substring(0, res.Length - 3);
        }

        public int Length() => lst.Count;
        
        public T this[int i]
        {
            get => lst[i];
            set => lst[i] = value;
        }

        public LstCollection<T> AddItem(T item)
        {
            lst.Add(item);
            return this;
        }

        public LstCollection<T> Sort(string field)
        {
            try
            {
                this.lst = lst.OrderBy(e => e.GetType().GetProperty(field).GetValue(e, null)).ToList();
            }
            catch (Exception)
            {
                throw new ArgumentException("Wrong Field name!");
            }
            return this;
        }

        public List<T> Search(string subStr)
        {
            bool SearchPredicater(T e)
            {
                foreach (PropertyDescriptor prop in TypeDescriptor.GetProperties(e)) 
                    if (prop.GetValue(e).ToString().Contains(subStr)) return true;
                return false;
            }
            var filtered = Validation.ValidateSearch(lst.FindAll(SearchPredicater));
            return filtered;
        }

        public LstCollection<T> Delete(string id)
        {
            var n = lst.Find(x => x.Id == id);
            if (n != null) lst.Remove(n);
            return this;
        }
        
        public LstCollection<T> Edit(string id, string atter, string value)
        {
            var n = lst.Find(x => x.Id == id);
            if (n != null)
            {
                PropertyInfo propertyInfo = Validation.ValidateEdit(n.GetType().GetProperty(atter));
                propertyInfo.SetValue(n, Convert.ChangeType(value, propertyInfo.PropertyType), null);
            }
            return this;
        }
        
        public LstCollection<T> ReadTxtFile(string fileName)
        {
            var fileData = System.IO.File.ReadAllText(fileName).Split('=').ToList();
            foreach (var strObject in fileData) {
                T p = new T();
                bool b = false;
                var lstObjects = strObject.Substring(1, strObject.Length - 2).Split('\n').ToList();
                foreach (var field in lstObjects)
                {
                    try
                    {
                        var fieldValue = field.Split(':').ToList();
                        PropertyInfo propertyInfo = p.GetType().GetProperty(char.ToUpper(fieldValue[0][0]) + fieldValue[0].Substring(1));
                        propertyInfo.SetValue(p, Convert.ChangeType(fieldValue[1].Substring(1), propertyInfo.PropertyType), null);
                    }
                    catch (Exception e)
                    {
                        try
                        {
                            Console.WriteLine($"--{e.InnerException.Message}");
                            b = true;
                        }
                        catch (Exception) {Console.WriteLine($"--{e.Message}");}
                    }
                }
                if (string.IsNullOrEmpty(p.Id)) p.Id = Guid.NewGuid().ToString();
                if (!b) this.AddItem(p);
            }
            return this;
        }
        
        public void WriteTxtFile(string fileName)
        {
            using (TextWriter tw = new StreamWriter(fileName)) tw.WriteLine(this);
        }
        
        public void AddToTxtFile(string fileName)
        {
            using (StreamWriter tw = File.AppendText(fileName)) tw.WriteLine("=" + this.ToString());
        }
        
        public LstCollection<T> ReadJsonFile(string fileName)
        {
            using (StreamReader r = new StreamReader(fileName))
            {
                string json = r.ReadToEnd();
                var dictionarys = JsonConvert.DeserializeObject<List<Dictionary<string, string>>>(json);
                foreach (var v in dictionarys)
                {
                    try
                    {
                        T p = JsonConvert.DeserializeObject<T>(JsonConvert.SerializeObject( v ));
                        if (string.IsNullOrEmpty(p.Id)) p.Id = Guid.NewGuid().ToString();
                        this.AddItem(p);
                    }
                    catch (Exception e) { Console.WriteLine($"--{e.InnerException.Message}"); }
                }
            }
            return this;
        }
        
        public void WriteJsonFile(string fileName)
        {
            string json = JsonConvert.SerializeObject(this.lst.ToArray());
            System.IO.File.WriteAllText(fileName, json);
        }
    }
}
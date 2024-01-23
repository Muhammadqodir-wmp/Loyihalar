using System;
using MySql.Data.MySqlClient;
using System.Windows.Forms;

namespace Oshxonamenyu
{
    public partial class Form1 : Form
    {
        private dishesForm _dishesForm;
        private Choy choyForm;
        private MySqlConnection connection; // Move MySqlConnection declaration to the class level

        public Form1()
        {
            InitializeComponent();
            _dishesForm = new dishesForm();
            choyForm = new Choy();
            connection = new MySqlConnection("server=localhost " +
                "database=oshxona;" +
                "uid=root;" +
                "password=;");
        }

        // Remove the Main method, it is not needed in a Windows Forms application

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
            _dishesForm.Show();

        }

        private void button2_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            this.Hide();
            choyForm.Show();

        }
    }
}

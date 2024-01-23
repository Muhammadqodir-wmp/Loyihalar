using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Oshxonamenyu
{
    public partial class Hisob2 : Form
    {
        private MySqlConnection sqlConnection;
        private string connectionString = "server=localhost;database=oshxona;uid=root;password=;";

        public Hisob2()
        {
            InitializeComponent();
            sqlConnection = new MySqlConnection(connectionString);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                sqlConnection.Open();


                string choyQuery = "SELECT *, miqdori * narxi AS jami_narxi FROM choy where miqdori > 0 " +
                    "UNION " +
                    "SELECT *, miqdori * narxi AS jami_narxi FROM taomlar where miqdori > 0  ";

                MySqlCommand sqlCommand = new MySqlCommand(choyQuery, sqlConnection);
                MySqlDataAdapter sqlDataAdapter = new MySqlDataAdapter(sqlCommand);

                DataTable mergedTable = new DataTable();
                sqlDataAdapter.Fill(mergedTable);

                int sum = 0;

                foreach (DataRow row in mergedTable.Rows)
                {
                    listBox1.Items.Add($"Nomi: {row["nomi"]}");
                    listBox2.Items.Add($"Narxi: {row["narxi"]}");
                    listBox3.Items.Add($"Miqdori: {row["miqdori"]}");
                    listBox4.Items.Add($"Jami narxi: {row["jami_narxi"]}");
                    sum += Convert.ToInt32(row["jami_narxi"]);
                }

                listBox4.Items.Add("Yakuniy summa: " + sum.ToString());
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
            finally
            {
                sqlConnection.Close();
            }
        }
    }
}

import Sidebar from "../components/Sidebar";
import { motion } from "framer-motion";

function Dashboard() {

  return (

    <div className="flex">

      <Sidebar />

      <div className="ml-64 p-10 w-full bg-gray-100 min-h-screen">

        <h1 className="text-3xl font-bold mb-8">
          Compliance Dashboard
        </h1>

        <div className="grid grid-cols-3 gap-8">

          <motion.div
            whileHover={{ scale:1.05 }}
            className="bg-white p-6 rounded-xl shadow-lg"
          >
            <h2 className="text-lg font-semibold">
              Compliance Score
            </h2>

            <p className="text-gray-600 mt-2">
              AI calculated DPDP compliance score
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale:1.05 }}
            className="bg-white p-6 rounded-xl shadow-lg"
          >
            <h2 className="text-lg font-semibold">
              Policy Upload
            </h2>

            <p className="text-gray-600 mt-2">
              Upload privacy policy for analysis
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale:1.05 }}
            className="bg-white p-6 rounded-xl shadow-lg"
          >
            <h2 className="text-lg font-semibold">
              Reports
            </h2>

            <p className="text-gray-600 mt-2">
              View compliance reports
            </p>
          </motion.div>

        </div>

      </div>

    </div>

  );
}

export default Dashboard;
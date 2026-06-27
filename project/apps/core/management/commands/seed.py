"""Seed the database with rich content matching the NexForge content pack.

Idempotent: uses ``get_or_create`` so re-running won't duplicate rows.
"""

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import BlogCategory, BlogPost
from apps.content.models import FAQ, Award, Download, Testimonial, GalleryItem
from apps.core.models import Client, Industry, Technology
from apps.projects.models import Project, ProjectDeliverable, ProjectMilestone
from apps.services.models import Service, ServiceBenefit, ServiceDeliverable


class Command(BaseCommand):
    help = "Load production-grade demo data matching the NexForge content pack."

    def handle(self, *args, **options):
        # --- Default Admin User --------------------------------------------------
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@nexforgeautomation.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_unusable_password()
            admin_user.save()

        # --- User Roles (Groups) -------------------------------------------------
        role_data = {
            "Admin": ["add", "change", "delete", "view"],
            "Editor": ["add", "change", "view"],
            "Viewer": ["view"],
        }
        for role_name, perms in role_data.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                for model in (Project, ProjectDeliverable, Industry, Technology, Client,
                              Service, ServiceBenefit, ServiceDeliverable,
                              BlogPost, BlogCategory, FAQ, Award, Download,
                              Testimonial, GalleryItem):
                    ct = ContentType.objects.get_for_model(model)
                    for action in perms:
                        try:
                            permission = Permission.objects.get(
                                content_type=ct,
                                codename=f"{action}_{model._meta.model_name}",
                            )
                            group.permissions.add(permission)
                        except Permission.DoesNotExist:
                            pass

        # --- Industries ----------------------------------------------------------
        industry_names = [
            "Automotive", "Pharmaceutical", "Food Processing", "Cement",
            "Steel", "Logistics", "FMCG", "Electronics",
            "Energy", "Water Treatment", "Mining", "Oil & Gas",
            "Textiles", "Packaging", "Warehouse Automation", "Chemical",
        ]
        industries = {}
        for name in industry_names:
            ind, _ = Industry.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower().replace(" ", "-").replace("&", "and")},
            )
            industries[name.lower()] = ind

        # --- Technologies --------------------------------------------------------
        tech_data = {
            "PLC": ("automation", None),
            "SCADA": ("automation", None),
            "IIoT": ("software", None),
            "Robotics": ("automation", None),
            "Machine Vision": ("software", None),
            "AI Analytics": ("software", None),
            "Siemens TIA Portal": ("automation", "PLC"),
            "Allen Bradley Studio 5000": ("automation", "PLC"),
            "Mitsubishi GX Works": ("automation", "PLC"),
            "Schneider EcoStruxure": ("automation", "SCADA"),
            "ABB Robotics": ("automation", "Robotics"),
            "FANUC": ("automation", "Robotics"),
            "KUKA": ("automation", "Robotics"),
            "Universal Robots": ("automation", "Robotics"),
            "OpenCV": ("software", "Machine Vision"),
            "TensorFlow": ("software", "AI Analytics"),
            "Python": ("software", None),
            "PostgreSQL": ("software", None),
            "AWS IoT": ("software", "IIoT"),
            "Azure IoT": ("software", "IIoT"),
            "Grafana": ("software", "SCADA"),
            "InfluxDB": ("software", "IIoT"),
            "ROS": ("software", "Robotics"),
            "YOLO": ("software", "Machine Vision"),
            "Cognex": ("automation", "Machine Vision"),
            "Keyence": ("automation", "Machine Vision"),
            "WinCC": ("automation", "SCADA"),
            "Ignition SCADA": ("software", "SCADA"),
            "AutoCAD Electrical": ("software", None),
            "EPLAN": ("software", None),
            "Node-RED": ("software", "IIoT"),
            "MQTT": ("software", "IIoT"),
            "Modbus TCP": ("automation", None),
            "Ethernet/IP": ("automation", None),
            "PROFINET": ("automation", None),
            "OPC UA": ("automation", None),
        }
        techs = {}
        for name, (cat, parent) in tech_data.items():
            t, _ = Technology.objects.get_or_create(
                name=name,
                defaults={"category": cat},
            )
            techs[name] = t

        # --- Clients -------------------------------------------------------------
        client_data = [
            ("VoltEdge Electric Vehicles", "Automotive"),
            ("Medixa Pharmaceuticals", "Pharmaceutical"),
            ("Ultra Cement", "Cement"),
            ("Mega Packaging Industries", "Packaging"),
            ("Electronics Assembly Co.", "Electronics"),
            ("GreenFood Processing", "Food Processing"),
        ]
        clients = {}
        for name, ind_key in client_data:
            ind = industries.get(ind_key.lower())
            c, _ = Client.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower().replace(" ", "-").replace(".", ""), "industry": ind},
            )
            clients[name] = c

        # --- Services (all 10 from content pack) ---------------------------------
        services_data = [
            {
                "title": "PLC Programming & Industrial Control Systems",
                "slug": "plc-programming-industrial-control-systems",
                "short": "Developing intelligent PLC-based industrial control systems that automate manufacturing processes, improve production efficiency, and ensure reliable plant operations.",
                "detailed": """NexForge designs, develops, tests, and commissions advanced PLC automation systems for manufacturing industries. Our engineers build scalable automation architectures capable of integrating production equipment, sensors, conveyors, robotic systems, packaging machinery, process plants, and utility equipment into a centralized control platform.

We specialize in upgrading legacy automation systems while ensuring seamless communication between machines, production software, enterprise systems, and cloud monitoring platforms. Every project follows international industrial standards with complete documentation, testing, commissioning, and operator training.""",
                "order": 1,
                "techs": ["Siemens TIA Portal", "Allen Bradley Studio 5000", "Mitsubishi GX Works", "Schneider EcoStruxure", "Modbus TCP", "Ethernet/IP", "PROFINET", "OPC UA", "MQTT"],
                "industries": ["Automotive", "Food Processing", "Pharmaceutical", "Chemical", "Steel", "Cement", "Textiles", "Packaging", "Warehouse Automation", "Oil & Gas", "Water Treatment", "Electronics"],
                "benefits": [
                    "Increase Production Efficiency by 30%", "Reduce Manual Operations",
                    "Improve Product Quality", "Minimize Production Downtime",
                    "Reduce Human Error", "Faster Decision Making",
                    "Improve Machine Safety", "Increase Overall Equipment Effectiveness (OEE)",
                    "Reduce Maintenance Cost", "Higher Production Output",
                ],
                "deliverables": [
                    "PLC Software", "Electrical Drawings", "IO Configuration",
                    "Control Logic", "Alarm Configuration", "Interlock Logic",
                    "System Documentation", "Testing Reports", "Factory Acceptance Test",
                    "Site Acceptance Test", "Commissioning Report", "Training Manual",
                    "Operator Manual", "Maintenance Guide",
                ],
            },
            {
                "title": "SCADA Development",
                "slug": "scada-development",
                "short": "Real-time monitoring and control systems providing complete visibility into industrial operations through interactive dashboards.",
                "detailed": """Our SCADA solutions enable manufacturers to monitor every production parameter in real time. Engineers can visualize machine performance, monitor alarms, generate reports, optimize energy consumption, and remotely control industrial equipment from centralized control rooms or secure cloud platforms.""",
                "order": 2,
                "techs": ["WinCC", "Ignition SCADA", "Schneider EcoStruxure", "Grafana", "InfluxDB", "PostgreSQL", "Node-RED"],
                "industries": ["Automotive", "Food Processing", "Steel", "Energy", "Utilities", "Manufacturing", "Mining", "Oil & Gas"],
                "benefits": [
                    "Centralized Monitoring", "Remote Access", "Real-Time Alerts",
                    "Production Analytics", "Reduced Downtime", "Historical Reports",
                    "Energy Monitoring", "Better Decision Making",
                ],
                "deliverables": [
                    "SCADA Dashboard", "Alarm Management", "Production Reports",
                    "Trend Analysis", "User Management", "Historical Database",
                    "Mobile Dashboard", "Cloud Monitoring",
                ],
            },
            {
                "title": "Industrial IoT Solutions",
                "slug": "industrial-iot-solutions",
                "short": "Connecting machines, sensors, and production equipment to cloud platforms for intelligent manufacturing.",
                "detailed": """Industrial IoT enables factories to collect live machine data, monitor production, predict failures, optimize energy consumption, and improve operational efficiency using connected smart devices.""",
                "order": 3,
                "techs": ["AWS IoT", "Azure IoT", "MQTT", "Node-RED", "InfluxDB", "Grafana", "Python", "PostgreSQL"],
                "industries": ["Automotive", "Logistics", "Energy", "Food Processing", "Warehouse Automation", "Pharmaceutical"],
                "benefits": [
                    "Predictive Maintenance", "Real-Time Data", "Lower Downtime",
                    "Energy Optimization", "Cloud Monitoring", "Remote Diagnostics",
                    "Asset Tracking", "Machine Health Monitoring",
                ],
                "deliverables": [
                    "IoT Dashboard", "Cloud Integration", "Mobile Monitoring",
                    "Analytics Reports", "Sensor Integration", "Gateway Configuration",
                    "API Integration",
                ],
            },
            {
                "title": "Robotics Integration",
                "slug": "robotics-integration",
                "short": "Industrial robot programming, simulation, and integration for automated manufacturing.",
                "detailed": """NexForge integrates industrial robotic systems for welding, assembly, packaging, material handling, and quality inspection. We program and commission robots from all major manufacturers.""",
                "order": 4,
                "techs": ["ABB Robotics", "FANUC", "KUKA", "Universal Robots", "ROS", "Python", "Machine Vision"],
                "industries": ["Automotive", "Electronics", "Packaging", "Food Processing", "Logistics"],
                "benefits": [
                    "Faster Production", "Reduced Labor Cost", "Consistent Quality",
                    "24×7 Manufacturing", "High Precision", "Lower Errors",
                    "Improved Safety",
                ],
                "deliverables": [
                    "Robot Programming", "Simulation", "Safety Integration",
                    "Commissioning", "Training", "Maintenance",
                ],
            },
            {
                "title": "Machine Vision Inspection",
                "slug": "machine-vision-inspection",
                "short": "AI-powered visual inspection systems for automatic defect detection and quality assurance.",
                "detailed": """Our machine vision solutions leverage deep learning and traditional computer vision for automatic defect detection, barcode reading, OCR, dimensional measurement, and assembly verification.""",
                "order": 5,
                "techs": ["OpenCV", "Python", "YOLO", "TensorFlow", "Cognex", "Keyence", "Machine Vision"],
                "industries": ["Electronics", "Pharmaceutical", "Automotive", "Packaging", "Food Processing"],
                "benefits": [
                    "Automatic Defect Detection", "Quality Assurance", "Reduced Scrap",
                    "Improved Accuracy", "Barcode Reading", "OCR Inspection",
                    "AI Inspection",
                ],
                "deliverables": [
                    "Inspection Software", "Camera Calibration", "Defect Reports",
                    "AI Model", "Dashboard",
                ],
            },
            {
                "title": "Predictive Maintenance",
                "slug": "predictive-maintenance",
                "short": "AI-driven predictive maintenance solutions that forecast equipment failures before they happen.",
                "detailed": """Predictive maintenance uses machine learning models trained on equipment data to predict failures, optimize maintenance scheduling, and extend asset life.""",
                "order": 6,
                "techs": ["Python", "TensorFlow", "AI Analytics", "Grafana", "InfluxDB", "AWS IoT"],
                "industries": ["Automotive", "Cement", "Steel", "Energy", "Manufacturing", "Oil & Gas"],
                "benefits": [
                    "Reduce Equipment Failure", "Predict Machine Breakdown",
                    "Maintenance Scheduling", "Increase Equipment Life",
                    "Lower Repair Cost",
                ],
                "deliverables": [
                    "Machine Health Dashboard", "Prediction Reports",
                    "Alerts", "Maintenance Planner", "Analytics",
                ],
            },
            {
                "title": "Electrical Control Panel Manufacturing",
                "slug": "electrical-control-panel-manufacturing",
                "short": "Design and fabrication of industrial electrical control panels built to international standards.",
                "detailed": """We manufacture custom electrical control panels for industrial automation applications, built to IEC and UL standards with rigorous testing and certification.""",
                "order": 7,
                "techs": ["AutoCAD Electrical", "EPLAN", "Siemens", "Schneider EcoStruxure", "Modbus TCP"],
                "industries": ["Automotive", "Pharmaceutical", "Food Processing", "Cement", "Energy", "Water Treatment"],
                "benefits": [
                    "Reliable Control", "Industrial Safety", "Easy Maintenance",
                    "Expandable Design",
                ],
                "deliverables": [
                    "Control Panels", "Electrical Drawings", "Testing", "Commissioning",
                ],
            },
            {
                "title": "Energy Monitoring Solutions",
                "slug": "energy-monitoring-solutions",
                "short": "Real-time energy monitoring and analytics for reducing electricity costs and carbon footprint.",
                "detailed": """Energy monitoring solutions track power consumption across factory equipment, identify inefficiencies, and provide actionable insights for energy optimization.""",
                "order": 8,
                "techs": ["IIoT", "Grafana", "InfluxDB", "Python", "MQTT", "Node-RED"],
                "industries": ["Automotive", "Cement", "Steel", "Energy", "Food Processing", "Textiles"],
                "benefits": [
                    "Reduce Electricity Bills", "Monitor Energy Usage",
                    "Carbon Footprint Reports", "Peak Load Analysis",
                    "Energy Analytics",
                ],
                "deliverables": [
                    "Energy Dashboard", "Reports", "Alerts", "Monthly Analytics",
                ],
            },
            {
                "title": "Annual Maintenance Contracts",
                "slug": "annual-maintenance-contracts",
                "short": "Comprehensive annual maintenance for industrial automation systems with 24×7 support.",
                "detailed": """Our AMC program provides preventive maintenance, emergency support, software updates, and regular health checks for your automation infrastructure.""",
                "order": 9,
                "techs": ["PLC", "SCADA", "IIoT", "Robotics"],
                "industries": ["Automotive", "Pharmaceutical", "Food Processing", "Cement", "Steel", "Energy"],
                "benefits": [
                    "24×7 Support", "Preventive Maintenance", "Emergency Support",
                    "Software Updates", "Machine Health Checks",
                ],
                "deliverables": [
                    "Quarterly Inspection", "Monthly Reports", "Emergency Visits",
                    "Technical Support", "Documentation",
                ],
            },
            {
                "title": "Smart Factory Consulting",
                "slug": "smart-factory-consulting",
                "short": "Industry 4.0 roadmap, digital transformation strategy, and automation planning.",
                "detailed": """Our consulting team helps manufacturers develop a comprehensive Industry 4.0 roadmap covering technology selection, ROI analysis, automation planning, and implementation strategy.""",
                "order": 10,
                "techs": ["Python", "AI Analytics", "IIoT", "AWS IoT", "Azure IoT"],
                "industries": ["Automotive", "Pharmaceutical", "Food Processing", "Logistics", "Electronics", "Manufacturing"],
                "benefits": [
                    "Industry 4.0 Roadmap", "Digital Transformation",
                    "ROI Analysis", "Technology Selection",
                    "Automation Planning",
                ],
                "deliverables": [
                    "Factory Audit", "Automation Strategy", "Project Roadmap",
                    "Budget Planning", "Implementation Plan",
                ],
            },
        ]

        for sd in services_data:
            s, created = Service.objects.get_or_create(
                slug=sd["slug"],
                defaults={
                    "title": sd["title"],
                    "short_description": sd["short"],
                    "detailed_description": sd["detailed"],
                    "order": sd["order"],
                    "is_active": True,
                },
            )
            if created:
                for t_name in sd["techs"]:
                    if t_name in techs:
                        s.technologies.add(techs[t_name])
                for ind_key in sd["industries"]:
                    ind = industries.get(ind_key.lower())
                    if ind:
                        s.industries.add(ind)
                for b in sd["benefits"]:
                    ServiceBenefit.objects.create(service=s, text=b)
                for d in sd["deliverables"]:
                    ServiceDeliverable.objects.create(service=s, title=d)

        # --- Projects ------------------------------------------------------------
        projects_data = [
            {
                "title": "Smart EV Manufacturing Plant Automation",
                "slug": "smart-ev-manufacturing-plant-automation",
                "client": "VoltEdge Electric Vehicles",
                "industry": "Automotive",
                "status": "ongoing",
                "location": "Chakan, Pune",
                "project_value": 18.5,
                "duration": "16 Months",
                "team_size": 28,
                "is_featured": True,
                "overview": "Complete automation of an electric vehicle manufacturing plant with robotic welding stations, conveyor automation, battery assembly monitoring, predictive maintenance dashboards, and cloud-connected production analytics.",
                "challenges": "Low production efficiency, high manual dependency, inconsistent quality, and lack of centralized production monitoring.",
                "solution": "Develop a fully automated manufacturing ecosystem integrating PLC controllers, robotic arms, SCADA visualization, Industrial IoT sensors, AI analytics, and centralized reporting dashboards.",
                "techs": ["Siemens TIA Portal", "SCADA", "IIoT", "ABB Robotics", "Python", "PostgreSQL", "Machine Vision", "AI Analytics"],
                "deliverables": ["PLC Programming", "SCADA Dashboard", "Robot Programming", "IoT Integration", "Control Panels", "Production Dashboard", "Operator Training", "Documentation", "AMC Support"],
            },
            {
                "title": "Pharma Production Line Automation",
                "slug": "pharma-production-line-automation",
                "client": "Medixa Pharmaceuticals",
                "industry": "Pharmaceutical",
                "status": "ongoing",
                "location": "Hyderabad",
                "project_value": 9.8,
                "duration": "12 Months",
                "team_size": 16,
                "is_featured": True,
                "overview": "Automatic batch tracking, electronic batch records, vision inspection, production reports, and 21 CFR Part 11 compliance for pharmaceutical manufacturing lines.",
                "challenges": "Regulatory compliance requirements, manual batch record keeping, quality inconsistencies, and lack of real-time visibility.",
                "solution": "Implemented Allen Bradley PLC controls with WinCC SCADA, barcode tracking, vision inspection systems, and electronic batch records management.",
                "techs": ["Allen Bradley Studio 5000", "WinCC", "Python", "IIoT", "Machine Vision", "PLC"],
                "deliverables": ["PLC Programming", "SCADA Dashboard", "Vision Inspection", "Batch Records", "Production Reports", "Documentation", "Training"],
            },
            {
                "title": "Smart Food Processing Factory",
                "slug": "smart-food-processing-factory",
                "client": "GreenFood Processing",
                "industry": "Food Processing",
                "status": "ongoing",
                "location": "Coimbatore",
                "project_value": 7.2,
                "duration": "10 Months",
                "team_size": 14,
                "is_featured": False,
                "overview": "Automated mixing, packaging line, quality monitoring, and energy dashboard for a modern food processing facility.",
                "challenges": "Manual mixing inconsistencies, packaging bottlenecks, energy waste, and quality control gaps.",
                "solution": "Mitsubishi PLC controls, SCADA visualization, IoT sensors for quality monitoring, and cloud-based energy management dashboard.",
                "techs": ["Mitsubishi GX Works", "SCADA", "IIoT", "Grafana", "InfluxDB", "MQTT"],
                "deliverables": ["Automated Mixing", "Packaging Line", "Quality Monitoring", "Energy Dashboard", "Training", "Documentation"],
            },
            {
                "title": "Ultra Cement Plant Automation",
                "slug": "ultra-cement-plant-automation",
                "client": "Ultra Cement",
                "industry": "Cement",
                "status": "completed",
                "location": "Nalgonda",
                "project_value": 13.4,
                "duration": "14 Months",
                "team_size": 22,
                "is_featured": True,
                "overview": "Complete plant automation including SCADA monitoring, remote diagnostics, and centralized control for a cement manufacturing facility.",
                "challenges": "Aging control systems, high energy consumption, frequent downtime, and lack of operational visibility.",
                "solution": "Upgraded legacy PLC systems with modern Siemens controllers, deployed plant-wide SCADA, implemented remote diagnostics, and energy optimization.",
                "techs": ["Siemens TIA Portal", "SCADA", "WinCC", "IIoT", "Modbus TCP", "OPC UA"],
                "deliverables": ["PLC Upgrade", "SCADA System", "Remote Diagnostics", "Energy Optimization", "Control Room Setup", "Training"],
            },
            {
                "title": "Mega Packaging Industry Automation",
                "slug": "mega-packaging-industry-automation",
                "client": "Mega Packaging Industries",
                "industry": "Packaging",
                "status": "completed",
                "location": "Ahmedabad",
                "project_value": 6.7,
                "duration": "8 Months",
                "team_size": 12,
                "is_featured": False,
                "overview": "Automated conveyors, robotic packaging, barcode inspection, and warehouse integration for a large packaging facility.",
                "challenges": "Manual packaging bottlenecks, high labor costs, damage during handling, and warehouse inefficiency.",
                "solution": "Integrated robotic packaging cells, automated conveyor systems, barcode tracking, and WMS integration.",
                "techs": ["FANUC", "Machine Vision", "PLC", "IIoT", "Python"],
                "deliverables": ["Robot Integration", "Conveyor System", "Barcode Tracking", "Warehouse Integration", "Documentation"],
            },
            {
                "title": "Electronics Assembly Automation",
                "slug": "electronics-assembly-automation",
                "client": "Electronics Assembly Co.",
                "industry": "Electronics",
                "status": "completed",
                "location": "Noida",
                "project_value": 10.2,
                "duration": "11 Months",
                "team_size": 18,
                "is_featured": True,
                "overview": "Machine vision-guided robotic assembly, automated testing, and quality inspection for precision electronics manufacturing.",
                "challenges": "Microscopic component handling, tight tolerances, high defect rates, and slow manual assembly.",
                "solution": "Vision-guided robots for precision assembly, AI-powered inspection systems, and automated testing stations.",
                "techs": ["Machine Vision", "Robotics", "PLC", "IIoT", "OpenCV", "TensorFlow", "YOLO"],
                "deliverables": ["Robot Programming", "Vision System", "Testing Station", "Quality Dashboard", "Documentation", "Training"],
            },
        ]

        for pd in projects_data:
            ind = industries.get(pd["industry"].lower())
            client = clients.get(pd["client"])
            p, created = Project.objects.get_or_create(
                slug=pd["slug"],
                defaults={
                    "title": pd["title"],
                    "industry": ind,
                    "client": client,
                    "status": pd["status"],
                    "location": pd["location"],
                    "project_value": pd["project_value"],
                    "duration": pd["duration"],
                    "team_size": pd["team_size"],
                    "is_featured": pd["is_featured"],
                    "overview": pd["overview"],
                    "challenges": pd["challenges"],
                    "solution": pd["solution"],
                },
            )
            if created:
                for t_name in pd["techs"]:
                    if t_name in techs:
                        p.technologies.add(techs[t_name])
                for d_title in pd["deliverables"]:
                    ProjectDeliverable.objects.create(project=p, title=d_title)
            # Milestones for every project
            if not p.milestones.exists():
                ProjectMilestone.objects.create(project=p, title="Requirements & Site Audit", description="Factory visit and requirement gathering", date=timezone.now() - timezone.timedelta(days=180), order=1)
                ProjectMilestone.objects.create(project=p, title="Engineering & Design", description="System architecture design and component selection", date=timezone.now() - timezone.timedelta(days=150), order=2)
                ProjectMilestone.objects.create(project=p, title="Development & Integration", description="PLC programming, panel manufacturing, and integration", date=timezone.now() - timezone.timedelta(days=90), order=3)
                ProjectMilestone.objects.create(project=p, title="Testing & Commissioning", description="Factory Acceptance Test and Site Acceptance Test", date=timezone.now() - timezone.timedelta(days=30), order=4)

        # --- Blog Categories & Posts --------------------------------------------
        blog_categories = [
            "Industry 4.0", "Robotics", "Industrial IoT",
            "Smart Manufacturing", "AI & Machine Learning",
            "Cybersecurity", "Energy Efficiency", "Case Studies",
        ]
        cat_objs = {}
        for name in blog_categories:
            cat, _ = BlogCategory.objects.get_or_create(name=name)
            cat_objs[name] = cat

        blog_posts = [
            {
                "title": "Revolutionizing Manufacturing with Industry 4.0",
                "slug": "revolutionizing-manufacturing-with-industry-4-0",
                "summary": "Explore how Industry 4.0 is transforming traditional manufacturing processes into smart, interconnected ecosystems.",
                "body": """Industry 4.0 represents the fourth industrial revolution, characterized by the fusion of digital technologies with physical manufacturing systems. This transformation is reshaping how factories operate, bringing unprecedented levels of efficiency, flexibility, and intelligence to production environments.

## Key Technologies Driving Industry 4.0

The Industrial Internet of Things (IIoT) forms the backbone of smart manufacturing, connecting machines, sensors, and systems to collect and analyze data in real time. Cloud computing enables scalable data storage and advanced analytics, while artificial intelligence and machine learning provide predictive capabilities that anticipate maintenance needs and optimize production parameters.

## Benefits for Manufacturers

Manufacturers adopting Industry 4.0 principles typically see significant improvements in operational efficiency, with reduced downtime, higher quality output, and lower energy consumption. Real-time visibility across the production floor enables faster decision-making and more agile responses to changing market demands.

## The Path Forward

At NexForge, we help manufacturers navigate their Industry 4.0 journey with practical, scalable solutions that deliver measurable results from day one.""",
                "category": "Industry 4.0",
                "author_name": "Arjun Reddy",
                "is_featured": True,
            },
            {
                "title": "The Role of AI in Modern Manufacturing",
                "slug": "role-of-ai-in-modern-manufacturing",
                "summary": "How artificial intelligence is revolutionizing quality control, predictive maintenance, and production optimization.",
                "body": """Artificial intelligence is rapidly becoming a cornerstone of modern manufacturing. From computer vision systems that inspect products at line speed to machine learning models that predict equipment failures before they occur, AI is delivering tangible value across the factory floor.

## Quality Control

AI-powered vision inspection systems can detect defects that are invisible to the human eye, operating 24/7 with consistent accuracy. Deep learning models continuously improve their detection capabilities, reducing false positives and catching new defect types as they emerge.

## Predictive Maintenance

By analyzing sensor data from production equipment, machine learning models can identify patterns that precede failures, enabling maintenance teams to intervene before breakdowns occur. This reduces unplanned downtime and extends equipment life.""",
                "category": "AI & Machine Learning",
                "author_name": "Priya Sharma",
            },
            {
                "title": "Enhancing Production with Robotic Integration",
                "slug": "enhancing-production-with-robotic-integration",
                "summary": "Discover how industrial robots are transforming production lines with precision, speed, and flexibility.",
                "body": """Industrial robotics has evolved far beyond simple pick-and-place operations. Today's robots are collaborative, intelligent, and adaptable, capable of handling complex tasks with precision and consistency.

## Types of Industrial Robots

From articulated robots for welding and assembly to delta robots for high-speed packaging, the range of robotic solutions available today can address virtually any manufacturing challenge.""",
                "category": "Robotics",
                "author_name": "Vikram Patel",
            },
            {
                "title": "Benefits of Real-Time Data in Industrial IoT",
                "slug": "benefits-of-real-time-data-industrial-iot",
                "summary": "How real-time data from connected devices is enabling smarter decision-making on the factory floor.",
                "body": """The Industrial Internet of Things (IIoT) is transforming manufacturing by providing real-time visibility into every aspect of production. Sensors, controllers, and connected devices generate streams of data that, when properly analyzed, reveal insights that drive better decisions.""",
                "category": "Industrial IoT",
                "author_name": "Anita Desai",
            },
            {
                "title": "Ensuring Cybersecurity in Smart Factories",
                "slug": "ensuring-cybersecurity-smart-factories",
                "summary": "Best practices for protecting industrial control systems and connected manufacturing environments.",
                "body": """As factories become more connected, cybersecurity becomes increasingly critical. Industrial control systems that were once air-gapped are now connected to enterprise networks and the cloud, creating new attack surfaces that must be protected.""",
                "category": "Cybersecurity",
                "author_name": "Rajesh Kumar",
            },
            {
                "title": "Energy Efficiency Practices in Industrial Automation",
                "slug": "energy-efficiency-industrial-automation",
                "summary": "How automation technologies can help reduce energy consumption and carbon footprint in manufacturing.",
                "body": """Energy efficiency is a growing priority for manufacturers, driven by both cost pressures and environmental regulations. Industrial automation technologies offer powerful tools for monitoring, analyzing, and optimizing energy usage across production facilities.""",
                "category": "Energy Efficiency",
                "author_name": "Sonali Gupta",
            },
        ]

        # Ensure author users exist for blog posts
        author_names = {bp["author_name"] for bp in blog_posts}
        author_users = {}
        for aname in author_names:
            username = aname.lower().replace(" ", ".")
            u, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": aname.split()[0],
                    "last_name": " ".join(aname.split()[1:]),
                    "email": f"{username}@nexforgeautomation.com",
                    "is_staff": False,
                },
            )
            if _:
                u.set_unusable_password()
                u.save()
            author_users[aname] = u

        for bp in blog_posts:
            cat = cat_objs.get(bp["category"])
            author = author_users.get(bp["author_name"], admin_user)
            BlogPost.objects.get_or_create(
                slug=bp["slug"],
                defaults={
                    "title": bp["title"],
                    "summary": bp["summary"],
                    "body": bp["body"],
                    "category": cat,
                    "author": author,
                    "is_featured": bp.get("is_featured", False),
                    "published_at": timezone.now(),
                },
            )

        # --- FAQs ----------------------------------------------------------------
        faqs_data = [
            ("What is industrial automation?", "Industrial automation involves using control systems, such as computers or robots, for handling different processes and machinery in an industry to replace human intervention.", FAQ.Category.GENERAL),
            ("How can I request a consultation?", "You can request a consultation by clicking on the 'Request Consultation' button on our homepage or by contacting us directly through our contact page.", FAQ.Category.GENERAL),
            ("What industries do you serve?", "We serve a variety of industries, including automotive, pharmaceuticals, food processing, electronics, cement, steel, logistics, FMCG, and more.", FAQ.Category.GENERAL),
            ("What is the typical project timeline?", "Project timelines vary based on scope and complexity. Typical automation projects range from 3 to 18 months from concept to commissioning.", FAQ.Category.GENERAL),
            ("Do you offer ongoing support?", "Yes, we provide comprehensive annual maintenance contracts (AMC) with 24x7 technical support, preventive maintenance, and emergency service.", FAQ.Category.GENERAL),
            ("What is your project delivery process?", "Our process follows four phases: Discover (factory audit & requirements), Design (engineering & planning), Deploy (implementation & commissioning), and Optimize (support & continuous improvement).", FAQ.Category.GENERAL),
            ("What are the benefits of predictive maintenance?", "Predictive maintenance helps in reducing equipment failures, predicting machine breakdowns, scheduling maintenance, increasing equipment life, and lowering repair costs.", FAQ.Category.SERVICE),
            ("Which PLC platforms do you support?", "We program and support all major PLC platforms including Siemens TIA Portal, Allen Bradley Studio 5000, Mitsubishi GX Works, Schneider EcoStruxure, Omron, and ABB.", FAQ.Category.SERVICE),
            ("Can you integrate with existing systems?", "Yes, we specialize in integrating new automation systems with legacy equipment using industrial communication protocols like Modbus TCP, PROFINET, EtherNet/IP, and OPC UA.", FAQ.Category.SERVICE),
            ("What is your approach to robotic integration?", "We assess your production requirements, simulate the solution, program and integrate the robots, and provide comprehensive training for your operators and maintenance team.", FAQ.Category.SERVICE),
            ("How does IIoT benefit my factory?", "IIoT provides real-time visibility into machine performance, enables predictive maintenance, optimizes energy consumption, and delivers actionable production analytics through cloud-connected dashboards.", FAQ.Category.SERVICE),
            ("Do you provide training for our team?", "Yes, every project includes comprehensive training programs covering system operation, maintenance procedures, troubleshooting, and safety protocols.", FAQ.Category.SERVICE),
        ]

        for i, (q, a, cat) in enumerate(faqs_data):
            FAQ.objects.get_or_create(question=q, defaults={"answer": a, "category": cat, "order": i, "is_active": True})

        # --- Awards ---------------------------------------------------------------
        awards_data = [
            ("Best Industrial Automation Company 2023", 2023, "Recognized as the leading industrial automation company for innovation and project delivery excellence."),
            ("Excellence in Robotics Integration 2022", 2022, "Awarded for outstanding achievement in robotic system integration and manufacturing automation."),
            ("Industry 4.0 Pioneer Award 2021", 2021, "Honored for pioneering work in implementing Industry 4.0 technologies in Indian manufacturing."),
        ]
        for title, year, desc in awards_data:
            Award.objects.get_or_create(title=title, defaults={"year": year, "description": desc})

        # --- Downloads ------------------------------------------------------------
        downloads_data = [
            ("Company Profile 2025", Download.Type.PROFILE),
            ("Service Brochure — PLC & Automation", Download.Type.BROCHURE),
            ("Service Brochure — IIoT Solutions", Download.Type.BROCHURE),
            ("Project Case Study — EV Manufacturing", Download.Type.CASE_STUDY),
            ("Project Case Study — Pharma Automation", Download.Type.CASE_STUDY),
            ("Industry Report — Smart Manufacturing Trends", Download.Type.REPORT),
        ]
        for title, dtype in downloads_data:
            Download.objects.get_or_create(
                title=title,
                defaults={
                    "type": dtype,
                    "file": "downloads/placeholder.pdf",
                },
            )
        # Update existing downloads to use the actual placeholder file
        for d in Download.objects.filter(file="downloads/placeholder.pdf"):
            d.file.name = "downloads/placeholder.pdf"
            d.save(update_fields=["file"])

        # --- Testimonials ---------------------------------------------------------
        testimonials_data = [
            ("Anita Rao", "Plant Head, VoltEdge", "NexForge transformed our EV manufacturing line. Production efficiency improved by 35% and downtime reduced by 42%. Their engineering team's expertise in robotics and IIoT integration is world-class.", clients.get("VoltEdge Electric Vehicles")),
            ("Dr. Suresh Menon", "VP Engineering, Medixa Pharma", "The pharma production line automation project was executed flawlessly. The 21 CFR Part 11 compliance implementation was particularly impressive. Highly recommended.", clients.get("Medixa Pharmaceuticals")),
            ("Ramesh Agarwal", "Plant Director, Ultra Cement", "Our cement plant automation project delivered a 25% production increase and 30% reduction in downtime. The SCADA system gives us complete visibility into our operations.", clients.get("Ultra Cement")),
            ("Priya Mehra", "Operations Head, Mega Packaging", "The robotic packaging integration was seamless. Our throughput increased by 40% and product damage reduced significantly. NexForge's team was professional and responsive throughout.", clients.get("Mega Packaging Industries")),
            ("Vijay Deshmukh", "CEO, GreenFood Processing", "From initial consultation to final commissioning, NexForge demonstrated exceptional technical capability and project management. Our energy costs dropped by 18% after the IoT implementation.", clients.get("GreenFood Processing")),
        ]

        for author, designation, quote, client in testimonials_data:
            Testimonial.objects.get_or_create(
                author_name=author,
                defaults={
                    "client": client,
                    "designation": designation,
                    "quote": quote,
                    "is_active": True,
                },
            )

        # --- Gallery Items --------------------------------------------------------
        gallery_categories = [
            ("Industrial Automation", "Factory floor transformation showing complete automation line"),
            ("Robotics", "Robotic arm performing precision welding operations"),
            ("IoT Solutions", "SCADA dashboard displaying real-time production analytics"),
            ("Smart Factories", "Modern control room with multiple monitoring stations"),
            ("Industrial Automation", "Electrical control panel installation"),
            ("Robotics", "Robotic packaging cell in operation"),
            ("IoT Solutions", "IoT sensor installation on production equipment"),
            ("Smart Factories", "Engineers monitoring production from centralized control room"),
            ("Industrial Automation", "Automated conveyor system"),
            ("Robotics", "Collaborative robot working alongside operators"),
        ]

        for cat, title in gallery_categories:
            GalleryItem.objects.get_or_create(
                title=title,
                defaults={
                    "category": cat,
                    "image": "gallery/placeholder.jpg",
                    "order": 1,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed complete — NexForge content pack loaded."))

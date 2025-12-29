import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';
import '../config.dart';
import '../theme/app_theme.dart';
import '../widgets/shared_widgets.dart';

class ProjectDetailScreen extends StatefulWidget {
  final int projectId;

  const ProjectDetailScreen({Key? key, required this.projectId})
      : super(key: key);

  @override
  State<ProjectDetailScreen> createState() => _ProjectDetailScreenState();
}

class _ProjectDetailScreenState extends State<ProjectDetailScreen>
    with SingleTickerProviderStateMixin {
  Map<String, dynamic>? project;
  bool _isLoading = true;
  bool _hasError = false;
  String _errorMessage = '';

  final _storage = const FlutterSecureStorage();

  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _loadProjectDetails();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _loadProjectDetails() async {
    try {
      setState(() {
        _isLoading = true;
        _hasError = false;
      });

      final token = await _storage.read(key: 'api_token');
      if (token == null) {
        throw Exception('Authentication token not found');
      }

      final response = await http.get(
        Uri.parse('$API_BASE/mobile/projects/${widget.projectId}/'),
        headers: {'X-API-KEY': token},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          project = data;
          _isLoading = false;
        });
        _animationController.forward();
      } else {
        throw Exception('Failed to load project details: ${response.body}');
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _hasError = true;
        _errorMessage = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.gray50,
      appBar: AppBar(
        title: Text(
          project != null
              ? project!['name'] ?? 'Project Details'
              : 'Project Details',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.w700,
              ),
        ),
        leading: IconButton(
          icon: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppTheme.gray100,
              border: Border.all(color: AppTheme.gray300),
            ),
            child: const Icon(Icons.arrow_back, size: 20),
          ),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          if (project != null)
            IconButton(
              icon: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.accentBlue.withValues(alpha: 0.1),
                  border:
                      Border.all(color: AppTheme.accentBlue.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.refresh,
                  size: 20,
                  color: AppTheme.accentBlue,
                ),
              ),
              onPressed: _loadProjectDetails,
            ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const LoadingCard();
    }

    if (_hasError) {
      return EmptyState(
        icon: Icons.error_outline,
        title: 'Error Loading Project',
        message: _errorMessage,
        action: TextButton(
          onPressed: _loadProjectDetails,
          child: const Text('Retry'),
        ),
      );
    }

    if (project == null) {
      return const EmptyState(
        icon: Icons.assignment,
        title: 'Project Not Found',
        message: 'The requested project could not be found.',
      );
    }

    return FadeTransition(
      opacity: _fadeAnimation,
      child: SlideTransition(
        position: _slideAnimation,
        child: CustomScrollView(
          slivers: [
            SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  _buildStatusCard(),
                  const SizedBox(height: 16),
                  _buildProjectOverview(),
                  const SizedBox(height: 16),
                  _buildLocationCard(),
                  const SizedBox(height: 16),
                  _buildStatisticsCard(),
                  const SizedBox(height: 16),
                  if (project!['document'] != null) _buildDocumentationCard(),
                  if (project!['document'] != null) const SizedBox(height: 16),
                  _buildProjectMetadata(),
                  const SizedBox(height: 32),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusCard() {
    final status = project!['status'] ?? 'pending';
    final statusColor = _getStatusColor(status);
    final statusIcon = _getStatusIcon(status);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: statusColor.withValues(alpha: 0.1),
              border: Border.all(color: statusColor.withValues(alpha: 0.3)),
            ),
            child: Icon(
              statusIcon,
              color: statusColor,
              size: 32,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Project Status',
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        color: AppTheme.gray600,
                      ),
                ),
                const SizedBox(height: 4),
                Text(
                  status.toUpperCase(),
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: statusColor,
                      ),
                ),
              ],
            ),
          ),
          if (project!['chain_issued'] == true)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: AppTheme.successGreen,
                border: Border.all(color: AppTheme.successGreen),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(
                    Icons.verified,
                    color: Colors.white,
                    size: 16,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    'VERIFIED',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                        ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildProjectOverview() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.accentBlue.withValues(alpha: 0.1),
                  border:
                      Border.all(color: AppTheme.accentBlue.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.info_outlined,
                  color: AppTheme.accentBlue,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'Project Overview',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text(
            project!['name'] ?? 'Unnamed Project',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w700,
                ),
          ),
          if (project!['description'] != null &&
              project!['description'].isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              project!['description'],
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppTheme.gray700,
                    height: 1.5,
                  ),
            ),
          ],
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: _buildInfoItem(
                  'Species',
                  project!['species'] ?? 'Not specified',
                  Icons.park,
                  AppTheme.successGreen,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildInfoItem(
                  'Area',
                  '${project!['area'] ?? 'N/A'} ha',
                  Icons.landscape,
                  AppTheme.warningOrange,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLocationCard() {
    final hasCoordinates =
        project!['latitude'] != null && project!['longitude'] != null;

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.successGreen.withValues(alpha: 0.1),
                  border:
                      Border.all(color: AppTheme.successGreen.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.location_on,
                  color: AppTheme.successGreen,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  'Location Information',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          if (project!['location'] != null &&
              project!['location'].isNotEmpty) ...[
            Text(
              'Address',
              style: Theme.of(context).textTheme.labelLarge,
            ),
            const SizedBox(height: 4),
            Text(
              project!['location'],
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppTheme.gray700,
                  ),
            ),
            if (hasCoordinates) const SizedBox(height: 16),
          ],
          if (hasCoordinates) ...[
            Text(
              'GPS Coordinates',
              style: Theme.of(context).textTheme.labelLarge,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.gray50,
                      border: Border.all(color: AppTheme.gray200),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Latitude',
                          style:
                              Theme.of(context).textTheme.labelSmall?.copyWith(
                                    color: AppTheme.gray600,
                                  ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          project!['latitude'].toString(),
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    fontWeight: FontWeight.w500,
                                  ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.gray50,
                      border: Border.all(color: AppTheme.gray200),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Longitude',
                          style:
                              Theme.of(context).textTheme.labelSmall?.copyWith(
                                    color: AppTheme.gray600,
                                  ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          project!['longitude'].toString(),
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    fontWeight: FontWeight.w500,
                                  ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildStatisticsCard() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.primaryBlue.withValues(alpha: 0.1),
                  border:
                      Border.all(color: AppTheme.primaryBlue.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.analytics,
                  color: AppTheme.primaryBlue,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'Project Statistics',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: StatCard(
                  title: 'Project Area',
                  value: '${project!['area'] ?? '0'} ha',
                  icon: Icons.landscape,
                  color: AppTheme.warningOrange,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: StatCard(
                  title: 'Carbon Credits',
                  value:
                      project!['chain_issued'] == true ? 'Issued' : 'Pending',
                  icon: Icons.eco,
                  color: project!['chain_issued'] == true
                      ? AppTheme.successGreen
                      : AppTheme.gray500,
                ),
              ),
            ],
          ),
          if (project!['estimated_carbon'] != null ||
              project!['trees_planted'] != null) ...[
            const SizedBox(height: 12),
            Row(
              children: [
                if (project!['estimated_carbon'] != null)
                  Expanded(
                    child: StatCard(
                      title: 'Est. Carbon',
                      value: '${project!['estimated_carbon']} tCO₂',
                      icon: Icons.cloud,
                      color: AppTheme.accentBlue,
                    ),
                  ),
                if (project!['estimated_carbon'] != null &&
                    project!['trees_planted'] != null)
                  const SizedBox(width: 12),
                if (project!['trees_planted'] != null)
                  Expanded(
                    child: StatCard(
                      title: 'Trees Planted',
                      value: project!['trees_planted'].toString(),
                      icon: Icons.forest,
                      color: AppTheme.successGreen,
                    ),
                  ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildDocumentationCard() {
    final documentUrl = project!['document'];

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.warningOrange.withValues(alpha: 0.1),
                  border: Border.all(
                      color: AppTheme.warningOrange.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.photo_library,
                  color: AppTheme.warningOrange,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'Project Documentation',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Container(
            height: 200,
            width: double.infinity,
            decoration: BoxDecoration(
              color: AppTheme.gray100,
              border: Border.all(color: AppTheme.gray300),
            ),
            child: documentUrl.toLowerCase().contains('.jpg') ||
                    documentUrl.toLowerCase().contains('.jpeg') ||
                    documentUrl.toLowerCase().contains('.png')
                ? Image.network(
                    documentUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.error_outline,
                            size: 48,
                            color: AppTheme.gray500,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Failed to load image',
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                  color: AppTheme.gray600,
                                ),
                          ),
                        ],
                      ),
                    ),
                  )
                : Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.insert_drive_file,
                          size: 48,
                          color: AppTheme.gray500,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Document',
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: AppTheme.gray600,
                                  ),
                        ),
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildProjectMetadata() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: AppTheme.gray200),
        boxShadow: [
          BoxShadow(
            color: AppTheme.gray900.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppTheme.gray600.withValues(alpha: 0.1),
                  border: Border.all(color: AppTheme.gray600.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  Icons.info,
                  color: AppTheme.gray600,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                'Project Metadata',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          _buildMetadataItem('Project ID', project!['id'].toString()),
          if (project!['created'] != null)
            _buildMetadataItem('Created', _formatDate(project!['created'])),
          if (project!['updated'] != null)
            _buildMetadataItem(
                'Last Updated', _formatDate(project!['updated'])),
          if (project!['wallet'] != null)
            _buildMetadataItem('Wallet ID', project!['wallet'].toString()),
        ],
      ),
    );
  }

  Widget _buildInfoItem(
      String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.05),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: 8),
          Text(
            title,
            style: Theme.of(context).textTheme.labelSmall?.copyWith(
                  color: AppTheme.gray600,
                  fontWeight: FontWeight.w500,
                ),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetadataItem(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: AppTheme.gray600,
                  ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
            ),
          ),
        ],
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'approved':
        return AppTheme.successGreen;
      case 'pending':
        return AppTheme.warningOrange;
      case 'rejected':
        return AppTheme.errorRed;
      default:
        return AppTheme.gray500;
    }
  }

  IconData _getStatusIcon(String status) {
    switch (status.toLowerCase()) {
      case 'approved':
        return Icons.check_circle;
      case 'pending':
        return Icons.pending;
      case 'rejected':
        return Icons.cancel;
      default:
        return Icons.help_outline;
    }
  }

  String _formatDate(String dateString) {
    try {
      final date = DateTime.parse(dateString);
      return '${date.day}/${date.month}/${date.year}';
    } catch (e) {
      return dateString;
    }
  }
}

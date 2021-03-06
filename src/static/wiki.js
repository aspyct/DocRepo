angular.module('wiki', [])
	.controller('DocumentListController', function ($scope, $rootScope, $http) {
		$scope.reload = function () {
			$http.get('/documentList')
				.then(function (result) {
					$scope.documentList = result.data;
				});
		};
		
		$scope.preview = function (doc) {
			$rootScope.$broadcast('previewDocument', doc);
		};
		
		$scope.showVersions = function (doc) {
			$http.get('documentVersions/' + doc.shortname)
				.then(function (result) {
					$scope.versionList = result.data;
				})
		};
		
		$scope.closeVersions = function () {
			$scope.versionList = undefined;
		}
		
		$scope.documentList = [];
		$scope.reload();
	})
	.controller('InvoiceCounterController', function ($scope, $http) {
		$scope.generateInvoiceNumber = function () {
			$http.post('/invoiceNumber')
				.then(function (result) {
					if (result.data) {
						$scope.invoiceNumber = result.data.invoiceNumber;
					}
				})
		};
	})
	.controller('PreviewController', function ($scope, $rootScope, $sce) {
		var isImage = function (doc) {
			return doc !== undefined && doc.mimetype && doc.mimetype.match(/^image\//) !== null;
		};
		
		var isPdf = function (doc) {
			return doc !== undefined && doc.mimetype === 'application/pdf';
		}
		
		$scope.$on('previewDocument', function (event, doc) {
			if (isImage(doc)) {
				$scope.documentType = 'image';
			} else if (isPdf(doc)) {
				$scope.documentType = 'pdf';
			} else {
				$scope.documentType = undefined;
			}

			$scope.doc = doc;
			$scope.documentUrl = $sce.trustAsResourceUrl('document/' + doc.name);
		});
	});